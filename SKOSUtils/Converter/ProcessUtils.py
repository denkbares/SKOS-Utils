class ProcessUtils:
    @staticmethod
    def trim(s):
        if s.startswith("\"") or s.startswith("'"):
            s = s[1:]
        if s.endswith("\"") or s.endswith("'"):
            s = s[:len(s)-1]
        return s

    @staticmethod
    def separate_attr_val(s):
        pos = s.find(': ')
        if pos > -1:
            return s[:pos], ProcessUtils.trim(s[pos + 2:])
        else:
            return s