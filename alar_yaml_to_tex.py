import yaml

# Function to detect and selectively wrap Kannada words with LaTeX commands
def wrap_kannada_words(text):
    def is_kannada(char):
        return '\u0C80' <= char <= '\u0CFF'
    
    wrapped_text = ""
    buffer = ""
    in_kannada_block = False
    
    for char in text:
        if is_kannada(char):
            if not in_kannada_block:
                if buffer:  # Flush accumulated non-Kannada text
                    wrapped_text += buffer
                    buffer = ""
                in_kannada_block = True
            buffer += char
        else:
            if in_kannada_block:
                # Wrap accumulated Kannada text and flush buffer
                wrapped_text += f"\\begin{{kannada}}{buffer}\\end{{kannada}}"
                buffer = char
                in_kannada_block = False
            else:
                buffer += char
    
    # Flush remaining text in buffer
    if in_kannada_block:
        wrapped_text += f"\\begin{{kannada}}{buffer}\\end{{kannada}}"
    else:
        wrapped_text += buffer
    
    return wrapped_text

# Function to generate LaTeX document content as a string
def generate_latex_content(entries):
    document_content = ""
    for item in entries:
        # Process and add section title
        title = wrap_kannada_words(item['entry'])
        document_content += f"\\section*{{{title}}}\n\n"
        
        # Process and add phonetic info and definitions
        phonetic_info = wrap_kannada_words(f"Phonetic: {item['phone']}")
        document_content += f"{phonetic_info}\n\n"
        document_content += f"\\begin{{itemize}}\n"
        for definition in item['defs']:
            definition_text = wrap_kannada_words(definition['entry'])
            document_content += f"\\item {definition_text}\n\n"
        document_content += f"\\end{{itemize}}\n"
    
    return document_content

# Load YAML data from file
yaml_filename = 'alar.yml'
with open(yaml_filename, 'r', encoding='utf-8') as yamlfile:
    entries = yaml.safe_load(yamlfile)

# Generate LaTeX document string
latex_content = generate_latex_content(entries)

# Setup LaTeX document preamble and append generated content
latex_document = r'''
\documentclass[12pt,a4paper,twoside]{book}

\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\rightmark}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0pt}

\usepackage{silence}
\WarningFilter{latex}{Command \InputIfFileExists}

\usepackage{noto}
\usepackage{fontspec}
\usepackage{xunicode}
\newfontfamily{\kannadafont}{Noto Serif Kannada}
\usepackage{polyglossia}

\usepackage{fontawesome}
\usepackage[hyphens]{url}
\setmainlanguage{english}
\setotherlanguages{kannada}

% Main serif font for English (Latin alphabet) text
\setmainfont{Noto Serif}
\setsansfont{Noto Sans}
\setmonofont{Noto Mono}

\usepackage{graphicx} 
\begin{document}

\begin{titlepage}
    \centering
    \vfill
    {\bfseries\Huge
        \begin{kannada}ಅಲರ್\end{kannada}
        \vskip2cm
        \Large A Kannada-English dictionary
        \vskip2cm
        \Large V. Krishna\\
    }    
    \vfill
    \includegraphics[width=8cm]{alar.jpg} % also works with logo.pdf
    \vfill
    \vfill
\end{titlepage}

\newpage\null\thispagestyle{empty}\newpage

\newpage\null\thispagestyle{empty}\newpage

\section*{About}

Alar is an authoritative Kannada-English dictionary corpus created by V. Krishna. It contains over 150,000 Kannada words with over 240,000 English definitions. It is released as an open data corpus licensed under the Open Database License (ODC-ODbL).

\section*{V. Krishna}

V. Krishna started building his Kannada-English dictionary in the 1970s as a hobby project. This incredible endeavour spanning four decades has now evolved into an invaluable contribution to Kannada language. In addition to authoring the colossal dictionary, he single-handedly digitised his original manuscripts. In 2019, he open sourced the entire dictionary.

He is a resident of Bengaluru and spends his time working on his dictionary and other Kannada literature projects. He has recently started laying foundations for a new English-Kannada dictionary. He can be reached at vkrishna1411@yahoo.co.in.

\section*{Data}

In 2019, Zerodha collaborated with V. Krishna to open source and publish his dictionary online and awarded him a grant to support his work.

The entire corpus (© V. Krishna) is available on the Alar repository: https://github.com/alar-dict. It is licensed under ODC-ODbL.

\newpage\null\thispagestyle{empty}\newpage
'''

latex_document += latex_content
latex_document += r'\end{document}'

# Write to .tex file
tex_filename = 'alar_dict.tex'
with open(tex_filename, 'w', encoding='utf-8') as texfile:
    texfile.write(latex_document)
