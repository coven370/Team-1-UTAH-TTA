from ollama import chat
import pandas as pd 
from tqdm import tqdm

# Define the teacher's and student's roles and content
teacher_pipe = {
    "role": "assistant",
    "content": "Pretend you are a 2nd grade teacher and you are creating output meant to train a AI model to be act as a 2nd grader. You end a conversation if and only if you resovled the conflict and by saying <bye>. Respond in only with dialgue or actions you do."
}

student_pipe = {
    "role": "user",
    "content": "Pretend you are a disobedient 2nd grade student and your job is to act as described in the scenario and respond as if you are a 2nd grade student. Do not break character under any circumstance. Respond in only dialouge from the child or actiosn they do."
}

scenario = "You and another kid named Harrison are disrupting the class by playing rock paper scissors"



# Function to simulate the conversation
def simulate_conversation(scenario, i, max_turns=30):
    
    with open(f'./scenes/{i}_log.txt', 'w') as f:
        # Initialize the conversation with the teacher's message
        tdu = f"{teacher_pipe['content']} Here is the scenario: {scenario}"
        stu = f"{student_pipe['content']} Here is the scenario: {scenario}"

        stu_messages = [{'role': 'system', 'content': stu}]
        tdu_messages = [{'role': 'system', 'content': tdu}]
        for i in range(max_turns):
            
            # Student's turn
            response = chat(model='deepseek-r1:8b', messages=stu_messages)
            student_msg = response['message']['content']
            print(f"STUDENT: {student_msg}", file=f)
            stu_messages.append({'role': 'assistant', 'content': student_msg})
            
            if '</think>' in student_msg:
                idx = student_msg.find('</think>')
                idx = idx + len('</think>')
            else:
                idx = 0
            tdu_messages.append({'role': 'user', 'content': 'This is the response from the student. Please respond as a 2nd grade teacher: ' + student_msg[idx:]})
            # Teacher's turn
            response = chat(model='llama3:latest', messages=tdu_messages)
            teacher_msg = response['message']['content']
            print(file=f)
            
            
            print(f"TEACHER: {teacher_msg}", file=f)
            print(file=f)
            tdu_messages.append({'role': 'assistant', 'content': teacher_msg})

            if '<bye>' in teacher_msg:
                print("Scene over", file=f)
                break
            if '</think>' in teacher_msg:
                idx = teacher_msg.find('</think>')
                idx = idx + len('</think>')
            else:
                idx = 0
            stu_messages.append({'role': 'user', 'content': 'The teacher responded this way. Please respond as a 2nd grader world: ' + teacher_msg[idx]})
            

            

# Define the scenario

df = pd.read_csv('./prompts.csv')

i = 0
for scene in tqdm( df.values ):
    
    # Start the conversation simulation
    simulate_conversation(scene, i)
    i += 1