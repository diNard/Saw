class Asterisk:
    @staticmethod
    def blocks(before, string, after, first):
        if before and not first:
            join = True
            for item in before:
                if item != '*':
                    join = False
                    break
            if join:
                string = ''.join(before) + string
                before = []
        return [before, string, after]