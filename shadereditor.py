import tkinter as tk
from tkinter import filedialog, messagebox

class ShaderEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Shader Editor")
        self.master.geometry("800x600")

        self.text_editor = tk.Text(self.master)
        self.text_editor.pack(expand=True, fill="both")
        self.text_editor.bind("<KeyRelease>", self.highlight)
        self.text_editor.bind("<Control-s>", self.save_file)

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        # File menu
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)

        # Documentation menu
        self.doc_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Documentation", menu=self.doc_menu)
        self.doc_menu.add_command(label="GLSL", command=self.show_glsl_doc)
        self.doc_menu.add_command(label=".BSS", command=self.show_bss_doc)

        self.glsl_keywords = {"float", "vec2", "vec3", "vec4", "mat2", "mat3", "mat4",
                              "texture", "sampler2D", "samplerCube", "varying",
                              "gl_Position", "gl_FragColor", "uniform", "in", "out",
                              "void", "main", "if", "else", "for", "while", "return",
                              "true", "false", "int", "ivec2", "ivec3", "ivec4",
                              "uvec2", "uvec3", "uvec4", "dvec2", "dvec3", "dvec4",
                              "bool", "bvec2", "bvec3", "bvec4", "struct"}

        self.bss_keywords = {"$global_determinator", "$shader_vertex", "$shader_fragment",
                             "$begin", "$end", "$invalid_state", "$branch"}

        self.completion_list = list(self.glsl_keywords.union(self.bss_keywords))

    def new_file(self, event=None):
        self.text_editor.delete("1.0", tk.END)

    def open_file(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Shader Files", "*.bss")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_editor.delete("1.0", tk.END)
                self.text_editor.insert(tk.END, content)
        self.highlight()

    def save_file(self, event=None):
        pass

    def save_as_file(self, event=None):
        pass

    def highlight(self, event=None):
        self.text_editor.tag_remove("glsl", "1.0", tk.END)
        self.text_editor.tag_remove("bss", "1.0", tk.END)
        content = self.text_editor.get("1.0", tk.END)

        for word in content.split():
            if word in self.glsl_keywords:
                start = "1.0"
                while True:
                    start = self.text_editor.search(word, start, stopindex=tk.END)
                    if not start:
                        break
                    end = f"{start}+{len(word)}c"
                    self.text_editor.tag_add("glsl", start, end)
                    start = end

            if word in self.bss_keywords:
                start = "1.0"
                while True:
                    start = self.text_editor.search(word, start, stopindex=tk.END)
                    if not start:
                        break
                    end = f"{start}+{len(word)}c"
                    self.text_editor.tag_add("bss", start, end)
                    start = end

        self.text_editor.tag_config("glsl", foreground="blue")
        self.text_editor.tag_config("bss", foreground="green")

    def show_glsl_doc(self):
        tk.messagebox.showinfo("GLSL Documentation", """
GLSL (OpenGL Shading Language) is a high-level shading language used with OpenGL and Vulkan.

Some basic GLSL keywords include:
- float
- vec2, vec3, vec4
- mat2, mat3, mat4
- texture
- sampler2D, samplerCube
- varying
- gl_Position, gl_FragColor
- uniform
""")

    def show_bss_doc(self):
        tk.messagebox.showinfo(".BSS Documentation", """
.BSS is a custom shader language used in Pathos engine.

Some key .BSS elements include:
- $global_determinator
- $shader_vertex, $shader_fragment
- $begin, $end
- $invalid_state
- $branch
""")

def main():
    root = tk.Tk()
    app = ShaderEditorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
