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

    @property
    def locator(self):
        """
        Returns the best locator for this UIElement:
        id > name > first class > tag
        """
        if self.id:
            return f'By.id("{self.id}")'
        elif self.name:
            return f'By.name("{self.name}")'
        elif self.classes:
            # classes AttributeValueList veya list olabilir, önce string yap
            if isinstance(self.classes, str):
                first_class = self.classes.split()[0]
            elif isinstance(self.classes, (list, tuple)):
                first_class = str(self.classes[0])
            else:
                first_class = str(self.classes)
            return f'By.className("{first_class}")'
        else:
            # fallback
            return f'By.tagName("{self.tag}")'
