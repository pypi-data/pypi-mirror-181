from dataclasses import dataclass, field

@dataclass
class JobInstruction:
    reference: str
    patient_id: str
    case_id: str