class Card():
    COLORS = ['Red', 'Blue', 'Yellow', 'Green', 'White']
    MAX_NUMBER = 5
    def __init__(self,number,color,card_id):
        self.number = number
        self.color = color
        self.card_id = card_id

        assert color in self.COLORS
        assert 1 <= number <= self.MAX_NUMBER

    def check_equal(self, other_card):
        '''
        Verify if a certain card is equal to another card
        '''
        return self.number == other_card.number and self.color == other_card.color
    
    def check_hint(self, hint_type, hint_info):
        '''
        Verify if a certain card matches a certain hint
        Each hint contains information about the color or about the number
        '''

        if hint_type == 'C' and hint_info in self.COLORS:
            if self.color == "Rainbow":
                return True
            else:
                return self.color == hint_info
            
        elif hint_type == 'N' and 1 <= hint_info <= self.MAX_NUMBER:
            return self.number == hint_info
            
        else:
            raise ValueError("Not valid Hint!")