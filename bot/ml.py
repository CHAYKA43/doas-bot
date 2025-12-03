from difflib import SequenceMatcher

import json
import fortune
import random
import logging

doas = None

def register():
    # Loads the question-and-answer database
    db_file = "config/db.json"
    
    def load_db():
        try:
            with open(db_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_db(db):
        with open(db_file, "w", encoding="utf-8") as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
    
    db = load_db()
    
    # Finds the most similar question from the database
    def find_best_match(question):
        question = question.lower()
        best_match = None
        best_ratio = 0.5
        
        logging.info(f"Finding an answer to the question: {question}")
        
        for item in db:
            ratio = SequenceMatcher(None, question, item["question"]).ratio()
            logging.info(f"Comparison with: {item['question']} (match {ratio:.2f})")
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = item
            elif ratio == best_ratio and best_match:
                best_match = random.choice([best_match, item])
        
        if best_match:
            logging.info(f"Selected answer: {best_match['answer']} (match {best_ratio:.2f})")
        else:
            logging.info("No suitable answer was found.")
        
        return best_match
    
    
    # Checks a question-answer pair for duplicates
    def is_duplicate(question, answer):
        question = question.lower()
        answer = answer.strip()
        for item in db:
            if SequenceMatcher(None, question, item["question"]).ratio() > 0.9 and SequenceMatcher(None, answer,    item["answer"]).ratio() > 0.9:
                return True
        return False
    
    
    
    # Command to add a new question-answer pair
    @doas.message_handler(commands=["teach"])
    async def terach(message):
        if "=" not in message.text:
            await doas.reply_to(message, "Usage: /teach Question=Answer")
            return
        
        _, data = message.text.split("/teach", 1)
        question, answer = data.strip().split("=", 1)
        question = question.strip().lower()
        answer = answer.strip()
        
        if not is_duplicate(question, answer):
            db.append({"question": question, "answer": answer})
            save_db(db)
            logging.info(f"A new pair has been added: {question} = {answer}")
            await doas.reply_to(message, "Got it!")
        else:
            await doas.reply_to(message, "Such a question-answer pair already exists.")
    
    
    # Command to ask the bot a question
    @doas.message_handler(commands=["ask"])
    async def ask(message):
        _, question = message.text.split("/ask", 1)
        question = question.strip().lower()
        best_match = find_best_match(question)
        
        if best_match:
            await doas.reply_to(message, best_match["answer"])
        else:
            await doas.reply_to(message, "I don't know the answer to that.")
    
    
    # Sending a quote
    @doas.message_handler(commands=['quote'])
    async def quote(message):
        fortun = fortune.get_random_fortune('config/quotes.txt')
        
        await doas.reply_to(message,f'`{fortun}`')
