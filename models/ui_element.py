class UIElement:
    def __init__(
        self,
        tag,
        element_id,
        name,
        element_type,
        classes,
        aria_label,
        role,
        text
    ):
        self.tag = tag
        self.id = element_id
        self.name = name
        self.type = element_type
        self.classes = classes
        self.aria_label = aria_label
        self.role_attr = role
        self.text = text

        # Bu alanlar SONRA doldurulacak
        self.action = None      # INPUT / CLICK / SELECT
        self.semantic = None    # USER_INPUT / FORM_SUBMIT / NAVIGATION

    def __repr__(self):
        return (
            f"{self.tag} | "
            f"name={self.name} | "
            f"action={self.action} | "
            f"semantic={self.semantic}"
        )
