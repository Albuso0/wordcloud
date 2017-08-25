class Counter(dict):
    def __missing__(self, key):
        return 0

class Box():
    def __init__(self, x, y, w, h):
        self.x = x 
        self.y = y 
        self.w = w 
        self.h = h 
        
    def overlap(self, b):
        if self.x < b.x:
            is_overlap = (self.x + self.w) > b.x
        else:
            is_overlap = (b.x + b.w) > self.x
        
        if self.y < b.y:
            is_overlap = is_overlap and (self.y + self.h) > b.y
        else:
            is_overlap = is_overlap and (b.y + b.h) > self.y
        if(is_overlap):
            return True
        return False
    
    def overlap_any(self, boxes):
        for b in boxes:
            if self.overlap(b):
                return True
        return False

    def inside(self, box):
        if self.x > box.x and self.x + self.w < box.x + box.w and self.y > box.y and self.y + self.h < box.y + box.h:
            return True
        else:
            return False
