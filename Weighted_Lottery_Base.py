from sympy import symbols, sympify
import random
import time
import streamlit as st


def combination(list, count):
    if count == 0:
        return [[]]
    
    if len(list) == 0:
        return []
    l = []
    for i in range(len(list)):
        m = list[i]
        remLst = list[i+1:]
        for p in combination(remLst, count-1):
            l.append([m] + p)
    return l


def dfs(lst, counts, total_picks):
    if not lst or not counts:
        return False
    #종결조건1: 다음 리스트가 카운트해야하는 수보다 적을 때
    if len(lst[0]) < counts[0]:
        st.error(f"반례: {lst[0]}, {counts[0]}")
        return False
    
    #종결조건2: 마지막 리스트에 남은 수가 카운트해야하는 수보다 많을 때
    if len(lst) == 1 and counts[0] <= len(lst[0]):
        return True
    
    combinations = combination(lst[0], counts[0])
    for comb in combinations:
        new_picks = total_picks - counts[0]
        new_lst = [list(set(sublst) - set(comb)) for sublst in lst[1:]] 
        flag = dfs(new_lst, counts[1:], new_picks)
        if flag == False:
            st.error(f"반례: {comb}")
            return False

    return True





class Candidate:
    
    #누가 참여하는지 + 기본값
    def __init__(self, candidate_dict):
        """Initialize the candidate with name and initial values."""
        self.candidate_dict = candidate_dict
        self.polling_event = []
        self.var1 = ""
        self.var2_list = []
        self.formula_list = []    
    
    def parse_polling_formula(self, formula, var1, var2):
        # Define the symbols
        allowed_vars = symbols(f'{var1} {var2}')
        try:
            # Attempt to create an expression from the formula
            expression = sympify(formula)
            # Get all symbols in the expression
            expression_symbols = expression.free_symbols
            
            # Check if there are any symbols in the expression that are not in the allowed list
            is_valid = all(symbol in allowed_vars for symbol in expression_symbols)
            
            if not is_valid:
                # If invalid, reset to a default expression
                expression = sympify(f"{allowed_vars[0]}-{allowed_vars[0]}")
        except:
            expression = sympify(f"{allowed_vars[0]}-{allowed_vars[0]} + 1")  # Default expression
            is_valid = False                
        return expression, is_valid
    

    def add_polling_event(self, event_dict, prize_name, prize_count, formula, var1, var2):
        """Add a polling event and its evaluation."""
        self.polling_event.append(PollingEvent(event_dict, prize_name, prize_count))
        self.add_polling_evaluation(len(self.polling_event) - 1, formula, var1, var2)
        self.var1 = var1
        self.var2_list.append(var2)
        self.formula_list.append(formula)

    def get_polling_weight(self, event_index, parsing_formula, var1, var2):
        """Calculate polling weights based on the given formula."""
        event = self.polling_event[event_index]
        not_weighted = False
        if var1 == "" or var2 == "" or parsing_formula == "":
            not_weighted = True
        
        if not_weighted:
            polling_weight = {}
            for key in event.event_participants:
                polling_weight[key] = 1
            return polling_weight
        
        expression, is_valid = self.parse_polling_formula(parsing_formula, var1, var2)
        if not is_valid:
            polling_weight = {}
            for key in event.event_participants:
                polling_weight[key] = 1
            return polling_weight
        
        polling_weight = {}
        for key in event.event_participants:
            values = {var1: self.candidate_dict.get(key, 0), var2: event.event_participants[key]}
            substituted_expression = expression.subs(values)
            result = substituted_expression.evalf()
            polling_weight[key] = result
        return polling_weight

    def add_polling_evaluation(self, event_index, parsing_formula, var1, var2):
        polling_weight = self.get_polling_weight(event_index, parsing_formula, var1, var2)
        self.polling_event[event_index].get_event_evaluation(polling_weight)
        return self

    def __str__(self):
        """String representation of Candidate object."""
        details = ["Candidate", str(self.candidate_dict), "\nPolling Event"]
        details.extend(str(event) for event in self.polling_event)
        return "\n".join(details)
    def write_streamlit(self):
        for i in range(len(self.polling_event)):
            with st.expander(f"Polling Event{i+1}"):
                st.write(f"Polling Variables: {self.var1}, {self.var2_list[i]}")
                st.write(f"Polling Formula: {self.formula_list[i]}")
                st.write(f"Polling Result:")
                st.write(self.polling_event[i].event_evaluated)
                participants = list(self.polling_event[i].event_participants.keys())
                for j in participants:
                    st.write(f":gray[User {j}: x: {self.candidate_dict[j]}, y: {self.polling_event[i].event_participants[j]}]")
        return None        

class PollingEvent:
    def __init__(self, event_dict, prize_name, prize_count):
        print("hi")
        self.event_participants = event_dict
        self.prize_name = prize_name
        self.prize_count = prize_count
        self.event_evaluated = {}
    
    def get_event_evaluation(self, evaluation):
        self.event_evaluated = evaluation
        return self
    
    def __str__(self):
        return str(self.event_participants) + " " + self.prize_name + " " + str(self.prize_count) +"\nCalculate: " + str(self.event_evaluated)

class WeightedVote:

    def __init__(self, candidates, event_data):
        self.candidates = candidates
        self.total_picked_candidates = []
        self.event_data = event_data
    def do_weighted_vote(self, type = "One By One", sleep_time = None, duplicate = False):
        if type == "One By One":
            return self.poll_one_event(duplicate)
        elif type == "At Once":
            return self.spontaneous(sleep_time, duplicate)
        else:
            return "Invalid Type"
    
    @staticmethod
    def select_candidate(candidates_weights):
        total_weight = sum(candidates_weights.values())
        probabilities = {candidate: weight / total_weight for candidate, weight in candidates_weights.items()}
        candidates, probs = zip(*probabilities.items())
        selected_candidate = random.choices(candidates, weights=probs, k=1)[0]
        return selected_candidate
    
    def select_one_candidate(self, polling_index): #TODO
        selected_candidate = self.select_candidate(self.candidates.polling_event[polling_index].event_evaluated)

        return selected_candidate

    def poll_one_event(self, polling_index, sleep_time, prevent_duplicate, show_progress = False):
        #print("selected: " + str(self.total_picked_candidates))
        candidates = []

        for index in range(self.candidates.polling_event[polling_index].prize_count):
            selected_candidate = self.select_one_candidate(polling_index)
            while prevent_duplicate == True and selected_candidate in self.total_picked_candidates or selected_candidate in candidates:

                st.write(f":gray[중복 발생] {index+1}번째 당첨자: {selected_candidate} (이미 당첨됨)")
                if show_progress:
                    time.sleep(sleep_time)   
                selected_candidate = self.select_one_candidate(polling_index)
         
            st.write(f"{index+1}번째 당첨자: {selected_candidate}")
            candidates.append(selected_candidate)
            if prevent_duplicate:
                self.total_picked_candidates.append(selected_candidate)
            #print(f"Selected Candidate: {selected_candidate}")
            time.sleep(sleep_time)
        #print(candidates)
        return candidates
    
    def is_prevent_duplicate_possible(self):
        total_prizes = 0
        user_list = []
        for i in range(len(self.candidates.polling_event)):
            total_prizes += self.candidates.polling_event[i].prize_count
            user_list.append(list(self.candidates.polling_event[i].event_participants.keys()))
        prize_list = list(self.event_data["event_prize_count_list"])
        st.write(f"참가자 리스트: {user_list}")
        st.write(f"상품 리스트: {prize_list}")
        st.write(f"총 상품 수: {total_prizes}")
        return dfs(user_list, prize_list, total_prizes)

    def poll_all_events(self, sleep_time, prevent_duplicate, show_progress = False):
        poll_results = []
        for i in range(len(self.candidates.polling_event)):
            one_poll = self.poll_one_event(i, sleep_time, prevent_duplicate, show_progress)
            poll_results.append(one_poll)
            #print("####")
            #print(poll_results)
        return poll_results
    
    def announce_winner(self, poll_results):
        for i in range(len(poll_results)):
            print(f"Prize: {self.candidates.polling_event[i].prize_name}")
            print(f"Winners: {poll_results[i]}")
        print()
    def __str__(self):
        return str(self.weighted_vote)
    
    def purge(self):
        self.total_picked_candidates = []
        return self
    
    def verify_probability(self):
        st.title(f"이벤트 확률 검증: ")
        st.button("다시하기:")
        for i in range(len(self.candidates.polling_event)):

            total_weight = sum(self.candidates.polling_event[i].event_evaluated.values())

            #total_weight_rounded = f"{total_weight:.4f}"
            #st.write(f"Total Weight: {total_weight_rounded}")
            probabilities = {candidate: weight / total_weight for candidate, weight in self.candidates.polling_event[i].event_evaluated.items()}
            event_name = self.event_data["event_name_list"][i]
            with st.expander(f"{event_name} 참가자들의 당첨 확률:"):
                for candidate, probability in probabilities.items():
                    prob_percent = probability * 100
                    formatted_probability = f"{prob_percent:.2f}" 
                    st.write(f"{candidate}: {formatted_probability}%")
        
            how_many_trials = st.number_input("How many trials? (max = 10000)", value=100, step=1, min_value=1, max_value= 10000, key=f'trial_{i}', format="%d")
            winners = {}
            for _ in range(how_many_trials):
                selected_candidate = self.select_one_candidate(i)
                if selected_candidate in winners:
                    winners[selected_candidate] += 1
                else:
                    winners[selected_candidate] = 1
            st.write(f"{how_many_trials}번 반복 후 각 참가자들의 당첨 횟수: ")
            st.write(winners)
    
    def practice_polling(self):
        st.title("한번 투표해봅시다:")
        vote = st.button("투표하기")
        polling_radio = st.radio("전체 vs 단일 이벤트", options = ["전체: 중복 제외", "전체: 중복 허용", "단일 이벤트"], key = "polling_type", index = None, horizontal = True)
        if polling_radio == "단일 이벤트":
            col1, col2 = st.columns(2)

            with col1:
                polling_index = st.number_input("투표 이벤트 선택", value=0, step=1, min_value=0, max_value=len(self.candidates.polling_event)-1, key="polling_index", format="%d")
            with col2:
                sleep_time = st.number_input("투표 시간 간격 (0.1초 ~ 10초)", value=1.0, step=0.1, min_value=0.1, max_value = 10.0, key="sleep_time", format="%f")
            if vote:
                st.write("투표 결과: ")
                st.write(self.poll_one_event(polling_index, sleep_time, prevent_duplicate = False, show_progress= True))
                self.purge()
        elif polling_radio == "전체: 중복 제외":
            if self.is_prevent_duplicate_possible() == False:
                st.error("중복 제외 추첨이 불가능합니다.")
                st.stop()
            sleep_time = st.number_input("투표 시간 간격 (0.1초 ~ 10초)", value=1.0, step=0.1, min_value=0.1, max_value = 10.0, key="sleep_time", format="%f")
            if vote:
                st.write("투표 결과: ")
                st.write(self.poll_all_events(sleep_time, prevent_duplicate = True, show_progress = True))
                self.purge()
        elif polling_radio == "전체: 중복 허용":
            sleep_time = st.number_input("투표 시간 간격 (0.1초 ~ 10초)", value=1.0, step=0.1, min_value=0.1, max_value = 10.0, key="sleep_time", format="%f")
            if vote:
                st.write("투표 결과: ")
                st.write(self.poll_all_events(sleep_time, prevent_duplicate = False, show_progress = True))
                self.purge()