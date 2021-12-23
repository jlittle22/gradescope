from bs4 import BeautifulSoup

class GSQuestion():

    def __init__(self, qid, title, weight, children, parent_id, content, crop):
        '''Create a question object'''
        self.title = title
        self.qid = qid
        self.children = children
        self.weight = weight
        self.parent_id = parent_id
        self.content = content
        self.crop = crop
        

    def get_info(self):
        question_data = {
            "title" : self.title,
            "qid" : self.qid,
            "children" : self.children,
            "weight" : self.weight,
            "parent_id" : self.parent_id,
            "content" : self.content,
            "crop" : self.crop
        }

        return question_data

    def to_patch(self):
        children = [child.to_patch() for child in self.children]
        output = {'id': self.qid, 'title': self.title, 'weight': self.weight, 'crop_rect_list': self.crop}
        print('length of children:', len(self.children))
        if len(children) != 0:
            output['children'] = children
        return output
