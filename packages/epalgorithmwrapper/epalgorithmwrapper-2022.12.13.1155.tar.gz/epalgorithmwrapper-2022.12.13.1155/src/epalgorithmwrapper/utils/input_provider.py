class InputProvider:
    def get_input_type(self):
        """Return input type"""

    def get_mode(self):
        """Get mode"""
    
    def is_development_mode(self):
        """Is development mode"""

    def get_patient_id(self):
        pass

    def get_case_id(self):
        pass

    def get_reference(self):
        pass

    def skip_reports(self):
        pass

    def skip_download_upload(self):
        pass

    def get_input_resources_context(self):
        pass

    def __str__(self):
        return str(self.__dict__)

class StaticInputProvider(InputProvider):
    def __init__(self, mode, input_type, patient_id, case_id, 
            input_resources_context, 
            reference, skip_reports:bool=False, skip_download_upload:bool=False, 
            development_mode:bool=False) -> None:
        self.mode = mode
        self.input_type = input_type
        self.patient_id = patient_id
        self.case_id = case_id
        self.reference = reference
        self._skip_reports = skip_reports
        self._skip_download_upload = skip_download_upload
        self.development_mode = development_mode
        self.input_resources_context = input_resources_context

    def get_input_type(self):
        return self.input_type

    def get_mode(self):
        return self.mode

    def get_patient_id(self):
        return self.patient_id
    
    def get_case_id(self):
        return self.case_id
    
    def is_development_mode(self):
        return self.development_mode
    
    def get_reference(self):
        return self.reference
    
    def skip_reports(self):
        return self._skip_reports
    
    def skip_download_upload(self):
        return self._skip_download_upload
    
    def get_input_resources_context(self):
        return self.input_resources_context
