import os

def generate_java_files(scenarios, ui_elements, output_dir="generated_java"):

    pages_dir = os.path.join(output_dir, "pages")
    tests_dir = os.path.join(output_dir, "tests")

    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(tests_dir, exist_ok=True)

    # 1️⃣ Page Object classları
    for page_name in set(s.page_name for s in scenarios):
        page_elements = [el for el in ui_elements if el.page_name == page_name]
        class_name = f"{page_name.capitalize()}Page"

        lines = [f"import org.openqa.selenium.*;\nimport org.openqa.selenium.support.*;\n\n"]
        lines.append(f"public class {class_name} {{\n")
        lines.append("    private WebDriver driver;\n\n")

        # Element tanımları
        for el in page_elements:
            lines.append(f"    private WebElement {el.name};\n")

        lines.append(f"\n    public {class_name}(WebDriver driver) {{\n")
        lines.append("        this.driver = driver;\n")
        for el in page_elements:
            locator_type = "id"  # örnek, element locator'ına göre ayarlanabilir
            lines.append(f'        this.{el.name} = driver.findElement(By.{locator_type}("{el.id}"));\n')
        lines.append("    }\n\n")

        # Action metodları
        for el in page_elements:
            method_name = f"{el.action}_{el.name}"
            lines.append(f"    public void {method_name}(String value) {{\n")
            if el.action == "type":
                lines.append(f"        {el.name}.sendKeys(value);\n")
            elif el.action == "click":
                lines.append(f"        {el.name}.click();\n")
            lines.append("    }\n\n")

        lines.append("}\n")

        with open(os.path.join(pages_dir, f"{class_name}.java"), "w") as f:
            f.writelines(lines)

    # 2️⃣ Test Classları
    for scenario in scenarios:
        class_name = f"{scenario['title'].replace(' ', '')}Test"
        page_class_name = f"{scenario['page_name'].capitalize()}Page"
        lines = [
            "import org.junit.jupiter.api.*;\n",
            "import org.openqa.selenium.*;\n",
            "import org.openqa.selenium.chrome.ChromeDriver;\n\n",
            f"public class {class_name} {{\n",
            "    private WebDriver driver;\n",
            f"    private {page_class_name} page;\n\n",
            "    @BeforeEach\n",
            "    public void setUp() {\n",
            "        driver = new ChromeDriver();\n",
            f"        page = new {page_class_name}(driver);\n",
            "    }\n\n",
            "    @AfterEach\n",
            "    public void tearDown() {\n",
            "        driver.quit();\n",
            "    }\n\n",
            "    @Test\n",
            f"    public void {scenario['title'].replace(' ', '_')}() {{\n"
        ]

        # Senaryo adımları
        for step in scenario['steps']:
            action_line = f"        page.{step['action']}_{step.get('element_name', 'unknown')}('{step.get('data','')}');\n"
            lines.append(action_line)

        # Assertion placeholder
        lines.append("        // TODO: Add assertions based on expected result\n")

        lines.append("    }\n")
        lines.append("}\n")

        with open(os.path.join(tests_dir, f"{class_name}.java"), "w") as f:
            f.writelines(lines)
