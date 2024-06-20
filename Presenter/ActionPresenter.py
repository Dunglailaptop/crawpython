# presenter.py


class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.bind_update_button(self.update_label)

    def update_label(self):
        data = self.model.get_data()
        self.view.set_label_text(data)
    
    
    def remove_vietnamese_accents(text):
        # Chuyển đổi chuỗi thành dạng chuẩn NFD (Normalization Form D)
        normalized_text = unicodedata.normalize('NFD', text)
        # Loại bỏ các ký tự dấu (accent)
        without_accents = ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn')
        return without_accents

    def remove_spaces(text):
        # Loại bỏ khoảng cách
        return re.sub(r'\s+', '', text)

    def process_text(text):
        text_without_accents = remove_vietnamese_accents(text)
        text_without_spaces = remove_spaces(text_without_accents)
        return text_without_spaces
    