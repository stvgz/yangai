
from ai.dbconnection import get_engine
from ai.model.prompt import Prompt
# PromptManager to manage prompt CRUD operations
class PromptManager:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_prompt(self, prompt_text, active = True):
        prompt = Prompt(prompt_text=prompt_text, active=active)
        self.session.add(prompt)
        self.session.commit()
        return prompt

    def get_prompt(self, id):
        return self.session.query(Prompt).filter(Prompt.id == id).first()

    def get_all_prompts(self):
        return self.session.query(Prompt).all()

    def update_prompt(self, id, prompt_text, active = True):
        prompt = self.get_prompt(id)
        prompt.prompt_text = prompt_text
        prompt.active = active
        self.session.commit()
        return prompt

    def delete_prompt(self, id):
        prompt = self.get_prompt(id)
        self.session.delete(prompt)
        self.session.commit()
        return True

    def get_latest_active_prompt(self):
        return self.session.query(Prompt).filter(Prompt.active == True).order_by(Prompt.created_at.desc()).first()


    def close(self):
        self.session.close()
        return True


if __name__ == "__main__":
    # # init db
    # from dbconnection import get_engine
    engine = get_engine()
    # Base.metadata.create_all(engine)

    # Create a new prompt
    PM = PromptManager(engine)

    # prompt = PM.create_prompt(prompt_text)

    # print latest active prompt
    latest_prompt = PM.get_latest_active_prompt()
    print(latest_prompt.prompt_text)