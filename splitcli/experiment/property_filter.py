
regex_matchers = ['STRING_MATCHES', 'STRING_NOT_MATCHES']
number_matchers = ['NUMBER_EQUAL','NUMBER_NOT_EQUAL','NUMBER_GREATER_THAN','NUMBER_LESS_THAN','NUMBER_BETWEEN','NUMBER_NOT_BETWEEN']
list_matchers = ['STRING_IN_LIST', 'STRING_NOT_IN_LIST']
boolean_matchers = ['BOOLEAN_EQUAL']

class PropertyFilter(object):
    def __init__(self, property, matcher, operands):
        super(PropertyFilter, self).__init__()
        self.property = property
        self.matcher = matcher
        self.operands = operands

    def overlap(self, other):
        if self.property != other.property:
            return False
        if self.matcher in regex_matchers or other.matcher in regex_matchers:
            # Potentially supportable in future
            return True
        if self.matcher == 'STRING_NOT_IN_LIST' or other.matcher == 'STRING_NOT_IN_LIST':
            # Potentially supportable in future
            return True
        
        # Check strings
        other_strings = other.valid_strings()
        for value in self.valid_strings():
            if value in other_strings:
                return True
        
        # Check ranges
        for ((inc_s_low, s_low), (inc_s_high, s_high)) in self.valid_ranges():
            for ((inc_o_low, o_low), (inc_o_high, o_high)) in self.valid_ranges():
                if s_high > o_low and s_high < o_high:
                    return True
                if inc_s_high:
                    if inc_o_low and s_high == o_low:
                        return True
                    if inc_o_high and s_high == o_high:
                        return True
                if s_low > o_low and s_low < o_high:
                    return True
                if inc_s_low:
                    if inc_o_low and s_low == o_low:
                        return True
                    if inc_o_high and s_low == o_high:
                        return True
        # No overlap
        return False
        
    
    def is_number_matcher(self):
        return self.matcher in number_matchers
    
    def valid_strings(self):
        if self.matcher == 'STRING_IN_LIST' or self.matcher == 'BOOLEAN_EQUAL':
            return self.operands
        return []
    
    def valid_ranges(self):
        # Ranges of format ((is_inclusive, lower_limit), (is_inclusive, upper_limit))
        if self.matcher == 'NUMBER_EQUAL':
            value = self.operands[0]
            return [((True,value),(True,value))]
        if self.matcher == 'NUMBER_NOT_EQUAL':
            value = self.operands[0]
            return [((True,float('-inf')),(False,value)), ((False,value),(True,float('inf')))]
        if self.matcher == 'NUMBER_GREATER_THAN':
            value = self.operands[0]
            return [((False,value),(True,float('inf')))]
        if self.matcher == 'NUMBER_LESS_THAN':
            value = self.operands[0]
            return [((True,float('-inf')),(False,value))]
        if self.matcher == 'NUMBER_BETWEEN':
            lower = self.operands[0]
            upper = self.operands[1]
            return [((True,lower),(True,upper))]
        if self.matcher == 'NUMBER_NOT_BETWEEN':
            lower = self.operands[0]
            upper = self.operands[1]
            return [((True,float('-inf')),(False,lower)), ((False,upper),(True,float('inf')))]
        if self.matcher == 'STRING_IN_LIST':
            ranges = []
            for value in self.operands:
                float_value = self.get_float(value)
                if float_value is not None:
                    ranges.append(((True,float_value),(True,float_value)))
            return ranges

        # Not a number matcher
        return []
    
    def get_float(self, value):
        try:
            return float(value)
        except ValueError:
            return None