class Check:
    before_message = ""
    passed_message = ""
    failed_message = ""
    check_status = ""
    error_message = ""


class StandardOutputChecks:
    def __init__(self, string_check_type, nothing_else, expected_output, before_message, passed_message, failed_message,
                 consider_elements_order=None):
        self.string_check_type = string_check_type
        self.nothing_else = nothing_else
        self.expected_output = expected_output
        self.before_message = before_message
        self.passed_message = passed_message
        self.failed_message = failed_message
        self.check_status = None
        self.error_message = None
        self.consider_elements_order = consider_elements_order

    def __str__(self):
        return {
            "string_check_type": self.string_check_type,
            "nothing_else": self.nothing_else,
            "expected_output": self.expected_output,
            "before_message": self.before_message,
            "passed_message": self.passed_message,
            "failed_message": self.failed_message,
            "check_status": self.check_status,
            "error_message": self.error_message,
            "consider_elements_order": self.consider_elements_order
        }

    def __repr__(self):
        return {
            "string_check_type": self.string_check_type,
            "nothing_else": self.nothing_else,
            "expected_output": self.expected_output,
            "before_message": self.before_message,
            "passed_message": self.passed_message,
            "failed_message": self.failed_message,
            "check_status": self.check_status,
            "error_message": self.error_message,
            "consider_elements_order": self.consider_elements_order
        }.__str__()

    def repr_json(self):
        return {
            "string_check_type": self.string_check_type,
            "nothing_else": self.nothing_else,
            "expected_output": self.expected_output,
            "before_message": self.before_message,
            "passed_message": self.passed_message,
            "failed_message": self.failed_message,
            "check_status": self.check_status,
            "error_message": self.error_message,
            "consider_elements_order": self.consider_elements_order
        }


class OutputFileChecks:
    def __init__(self, file_name, string_check_type, nothing_else, expected_output, before_message, passed_message, failed_message,
                 consider_elements_order=None):
        self.file_name = file_name
        self.string_check_type = string_check_type
        self.nothing_else = nothing_else
        self.expected_output = expected_output
        self.before_message = before_message
        self.passed_message = passed_message
        self.failed_message = failed_message
        self.check_status = None
        self.error_message = None
        self.consider_elements_order = consider_elements_order

    def __str__(self):
        return {
            "file_name": self.file_name,
            "string_check_type": self.string_check_type,
            "nothing_else": self.nothing_else,
            "expected_output": self.expected_output,
            "before_message": self.before_message,
            "passed_message": self.passed_message,
            "failed_message": self.failed_message,
            "check_status": self.check_status,
            "error_message": self.error_message,
            "consider_elements_order": self.consider_elements_order
        }

    def __repr__(self):
        return {
            "file_name": self.file_name,
            "string_check_type": self.string_check_type,
            "nothing_else": self.nothing_else,
            "expected_output": self.expected_output,
            "before_message": self.before_message,
            "passed_message": self.passed_message,
            "failed_message": self.failed_message,
            "check_status": self.check_status,
            "error_message": self.error_message,
            "consider_elements_order": self.consider_elements_order
        }.__str__()
