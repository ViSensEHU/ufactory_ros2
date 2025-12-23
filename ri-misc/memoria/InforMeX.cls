\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{InforMeX}[2020/04/06]
\LoadClass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=0.7in, bmargin=1in, a4paper]{geometry}
\usepackage{graphicx}
\usepackage{float}
\usepackage{xcolor}
\usepackage{colortbl}
\usepackage{ifthen}
\usepackage{lipsum}
\usepackage[spanish]{babel}
\usepackage[none]{hyphenat} % no partir palabras entre diferentes línea con -

%\usepackage[backend=biber,style=footnote-dw]{biblatex}
\usepackage[backend=biber,style=numeric, sorting=none]{biblatex}
\addbibresource{referencias.bib} % Tu archivo .bib
\usepackage{hyperref}

\usepackage{enumitem}

\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}

\usepackage{svg}

\usepackage{comment}

\usepackage{multirow}
\usepackage{hhline}

\usepackage{float}
\newfloat{listing}{htbp}{}
\floatname{listing}{Código}

\usepackage{caption}



\usepackage{listings}
\lstset{
  language=Matlab,
  basicstyle=\ttfamily\scriptsize,
  keywordstyle=\color{blue},
  commentstyle=\color{gray},
  stringstyle=\color{orange},
  showstringspaces=false,
  breaklines=true,
  frame=single,
  captionpos=b,
  numbers=left,            % ← Añade números de línea a la izquierda
  numberstyle=\tiny\color{gray},  % ← Estilo de los números de línea
  stepnumber=1,            % ← Muestra cada línea (puedes usar 2, 5, etc.)
  numbersep=5pt            % ← Espacio entre números y código
}

\renewcommand{\lstlistingname}{Código}
\renewcommand{\lstlistlistingname}{Índice de códigos}

\usepackage{csquotes}

%\setlength{\parindent}{12pt}
\setlength{\parindent}{0pt}

\definecolor{greyscale}{RGB}{128,128,128}
\definecolor{borgon}{HTML}{990033}
\definecolor{good_black}{RGB}{36, 30, 32}
\definecolor{good_green}{RGB}{109, 191, 81}

\usepackage{fontspec}
\setmainfont[
Path=Core/,
BoldFont=1.ttf,
ItalicFont=2.ttf,
BoldItalicFont=3.ttf,
]{4.ttf}
\newcommand*{\datos}[3]{
%%%%%%%%%%%%%%%%%%% Set instance to fc
\ifthenelse{\equal{#1}{color}}{
    \begin{flushleft}
        \vspace*{-0.6in}
        \begin{figure}[H]
        \hspace*{-0.567cm}
            \includegraphics[width=0.6\textwidth]{Images/ucm_uned.png}
        \end{figure}
    \end{flushleft}
}{
      \begin{flushleft}
        \vspace*{-0.6in}
        \begin{figure}[H]
        \hspace*{-0.567cm}
            \includegraphics[width=0.35\textwidth]{Images/UCMnegro.jpg}
        \end{figure}
    \end{flushleft}  
}
%%%%%%%%%%%%%%%%%%%   
%%%%%%%%%%%%%%%%%%% Set instance to sc
\begin{flushright}
\vspace*{-2.7cm}
\large
\textbf{\uppercase{ ROBÓTICA INDUSTRIAL#3}}\\\textbf{Trabajo final sobre la materia}
\end{flushright}
%%%%%%%%%%%%%%%%%%%
}
\newcommand*{\adaptar}[2]{
    \ifthenelse{\equal{#1}{si}}{
        \large
    }{}
    \ifthenelse{\equal{#2}{si}}{
        \pagecolor{good_black}
        \color{good_green}
    }{}
}

\newcommand*{\firma}[1]{
    \vfill
    \noindent
    \texttt{#1}
    \phantom{a}\\
    \phantom{a}\\
    \phantom{a}\\
    \phantom{a}\\
    \phantom{a}\\
    \phantom{a}\\
    \phantom{a}\\
    \phantom{a}\\
    \phantom{a}\\
    \textbf{\today}
     \phantom{a}\\
    \phantom{a}\\
}
\newcommand*{\derechosUso}{
\vfill
\begin{center}
\small
        Queda prohibido copiar, reproducir, distribuir, publicar, transmitir, difundir, o en cualquier modo explotar cualquier parte de este servicio sin la autorización previa por escrito de la Universidad Complutense de Madrid o de los titulares correspondientes.
\end{center}
}

\newcommand*{\portada}[6]{ % #1=Máster, #2=Asignatura, #3=Alumno, #4=Curso, #5=Fecha, #6=Título del trabajo
    \thispagestyle{empty}
    \begin{center}
        \vspace*{2cm}
        \includegraphics[width=0.8\textwidth]{Images/ucm_uned.png}
        \vspace*{2cm}

        {\fontsize{30pt}{36pt}\selectfont \textbf{#6}}
        \vspace{2cm}

        {{\fontsize{24pt}{36pt}\selectfont \textbf{#1}} }
        \vspace{1cm}
        
        %{\fontsize{20pt}{36pt}\selectfont Asignatura:\textbf{#2}}
        {\fontsize{20pt}{36pt}\selectfont \textbf{Asignatura:} #2}
        \vspace{1cm}

        {\fontsize{20pt}{36pt}\selectfont \textbf{Curso:} #4}
        \vspace{5cm}

        {\Large \textbf{Alumno:} #3}
        \vspace{1cm}

        {\Large \textbf{#5}}

    \end{center}
    \newpage
}

\endinput