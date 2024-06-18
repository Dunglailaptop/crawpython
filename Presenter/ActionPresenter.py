# presenter.py

class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.bind_update_button(self.update_label)

    def update_label(self):
        data = self.model.get_data()
        self.view.set_label_text(data)
