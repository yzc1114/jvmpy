from .cp_symref import SymRef
from classfile.cp.cp_member_ref import ConstantMemberrefInfo


class MemberRef(SymRef):
    def __init__(self):
        super().__init__()
        self.name: str = None
        self.descriptor: str = None

    def copy_member_ref_info(self, member_info: ConstantMemberrefInfo):
        self.class_name = member_info.class_name()
        self.name, self.descriptor = member_info.name_and_descriptor()
