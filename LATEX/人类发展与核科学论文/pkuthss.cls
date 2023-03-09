% Peking University dissertation document class
%
% Copyright (c) 2008-2009 solvethis
% Copyright (c) 2010-2021 Casper Ti. Vector
% Copyright (c) 2021 Kurapica
% Copyright (c) 2021 iofu728
%
% This work may be distributed and/or modified under the conditions of the
% LaTeX Project Public License, either version 1.3 of this license or (at
% your option) any later version.
% The latest version of this license is in
%   https://www.latex-project.org/lppl.txt
% and version 1.3 or later is part of all distributions of LaTeX version
% 2005/12/01 or later.
%
% This work has the LPPL maintenance status `maintained'.
% The current maintainer of this work is Casper Ti. Vector.
%
% This work consists of the following files:
%   pkuthss.cls
%   pkuthss-gbk.def
%   pkuthss-utf8.def
%   pkulogo.eps
%   pkuword.eps

\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{pkuthss}
	[2020/11/02 v1.8.3 Peking University dissertation document class]

% eg. `\thss@int@boolopt{spacing}{true}' will expand to:
%   \newif\ifthss@opt@spacing \thss@opt@spacingtrue
%   \DeclareOption{spacing}{\thss@opt@spacingtrue}
%   \DeclareOption{nospacing}{\thss@opt@spacingfalse}
\def\thss@int@boolopt#1#2{
	\expandafter\newif\csname ifthss@opt@#1\endcsname
	\@nameuse{thss@opt@#1#2}
	\DeclareOption{#1}{\@nameuse{thss@opt@#1true}}
	\DeclareOption{no#1}{\@nameuse{thss@opt@#1false}}
}
% Process the encoding options.
\newif\ifthss@opt@gbk \thss@opt@gbktrue
\DeclareOption{GBK}{\thss@opt@gbktrue\PassOptionsToClass{GBK}{ctexbook}}
\DeclareOption{UTF8}{\thss@opt@gbkfalse\PassOptionsToClass{UTF8}{ctexbook}}
% Whether to enable `\Uppercase' (works problematically) in heading marks.
\thss@int@boolopt{uppermark}{false}
% Whether to modify fonts according to school regulation.
\thss@int@boolopt{pkufont}{true}
% Whether to modify footnote format according to school regulation.
\thss@int@boolopt{pkufoot}{true}
% Whether to modify spacing according to school regulation.
\thss@int@boolopt{pkuspace}{true}
% Whether to use some common settings for adjusting spacing.
\thss@int@boolopt{spacing}{true}
% Add PDF bookmark for table of contents.
\thss@int@boolopt{pdftoc}{true}
% Whether to enable the `\spacialchap' command.
\thss@int@boolopt{spechap}{true}
% Whether to automatically set up properties for generated PDF from user
% defined document information (author, title, etc.).
\thss@int@boolopt{pdfprop}{true}
% Whether to disable some infractions intended to make the style less ugly.
\thss@int@boolopt{ugly}{false}
% Pass all other options to `ctexbook' document class.
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{ctexbook}}
% Process all class options now.
\ProcessOptions\relax

% Prevent fontspec (loaded by xeCJK) from interfering with newtxmath.
\ifthss@opt@pkufont\PassOptionsToPackage{no-math}{fontspec}\fi
% Work around the `\lvert already defined' error.
% cf. <https://github.com/CTeX-org/ctex-kit/issues/454>.
\ifthss@opt@pkufont\RequirePackage{amsmath}\fi
% pkuthss is based on ctexbook; we use `xiao 4' as default font size.
\LoadClass[zihao = -4]{ctexbook}[2014/03/06]
% ctex 2.x no longer loads ifpdf and ifxetex by itself.
\RequirePackage{ifpdf, ifxetex}
% Provides support for `key = val' grammar.
\RequirePackage{keyval}
% Graphics support.
\RequirePackage{graphicx}[1999/02/16]
% Provides utilities for setting up page layout.
\RequirePackage{geometry}
% fancyhdr provides utilities for setting up headers and footers.
\RequirePackage{fancyhdr}
% Provides `\uline' used in `\maketitle' (but do not mess with `\emph').
\RequirePackage[normalem]{ulem}
% Provides tableofcontents setting.
\RequirePackage{titletoc}
% Provides cover the scanned version pdf.
\RequirePackage[absolute,overlay]{textpos}
\RequirePackage{color}
% `\AtEndOfClass' used to avoid `PDF destination not defined' with setspace.
\AtEndOfClass{\RequirePackage{hyperref}}

\ifthss@opt@gbk
	\input{pkuthss-gbk.def}
	\ifxetex
		% No support for XeLaTeX compilation in non-unicode encoding, i.e. GBK.
		\ClassError{pkuthss}%
			{XeLaTeX compilation is not supported without UTF-8}%
			{%
				XeLaTeX compilation without UTF-8 is very problematic.\MessageBreak
				Therefore please use UTF-8 encoding for the LaTeX code.%
			}
	\fi
\else
	\input{pkuthss-utf8.def}
\fi

\ifthss@opt@pkufont
	% Use Times New Roman / Arial according to school regulation.
	% Option used to prevent newtxtext from manipulating footnote marks.
	\RequirePackage[defaultsups]{newtxtext}
	\RequirePackage[cmintegrals, varg]{newtxmath}
\else
	% Provides `\Box' for originauth.tex if newtx is absent.
	\RequirePackage{latexsym}
\fi

\ifthss@opt@pkufoot
	% Handle the `Unparsed material' issue with latex/dvipdfmx compilation.
	\unless\ifxetex\unless\ifpdf
		\newcommand*\pgfsysdriver{pgfsys-dvipdfm.def}
	\fi\fi
	% Circled text, cf. <https://tex.stackexchange.com/questions/7032/>.
	\RequirePackage{tikz}
	\newcommand*\thss@int@circled[1]{%
		\scalebox{0.8}{\tikz[baseline = (char.base)]{
			\node[
				shape = circle, draw = black, minimum size = 1.25em, inner sep = 0pt
			] (char) {#1};
		}}%
	}
	% Use circled numbers as footnote symbols. Does not affect title page, but
	% footnote is rarely used in dissertation covers ;)
	\renewcommand*{\thefootnote}%
		{\protect\thss@int@circled{\arabic{footnote}}}
	% Provides utility to modify footnote spacing.
	% Option used to make sure it does not render interleaf pages totally blank.
	\RequirePackage[cleardoublepage = current]{scrextend}
	% Set up footnote spacing: whole paragraph indent 2 ccwd, 0.5 ccwd after mark.
	\deffootnote{2\ccwd}{0pt}{\thefootnotemark\hspace{0.5\ccwd}}
\fi

\ifthss@opt@pkuspace
	% lineskip / baselineskip = 20 bp / (12 bp * (6 / 5)).
	\linespread{1.39}\selectfont
	% Provides utilities for setting TOC format; `titles' applied to avoid
	% interfering with LaTeX's own title mechanism.
	\RequirePackage[titles]{tocloft}
	\setlength{\cftbeforechapskip}{6bp plus 1bp}
	\setlength{\cftsecindent}{\ccwd}
	\setlength{\cftsubsecindent}{2\ccwd}
	\setlength{\cftsubsubsecindent}{4\ccwd}
	% `caption' modifies font size and separator of captions.  `subcaption'
	% provides functions similar to `subfigure'/`subfig' but does not clash with
	% `tocloft'; it clashes with `subfigure'/`subfig', but the error message will
	% say they cannot be used simultaneously.
	\RequirePackage{caption, subcaption}
	\ifthss@opt@ugly
		\DeclareCaptionFont{capfsize}{\fontsize{11bp}{13.2bp}}
	\else
		\DeclareCaptionFont{capfsize}{\zihao{5}}
	\fi
	\DeclareCaptionLabelSeparator{quad}{\quad}
	\captionsetup{font = capfsize, labelsep = quad}
	\captionsetup[sub]{font = capfsize}
\fi

\ifthss@opt@spacing
	% Make spacing nicer in some situations (eg. footnotes and verbatims).
	\RequirePackage{setspace}
	% Remove superfluous spacing between footnotes.
	\setlength{\footnotesep}{0pt}
	% Lists often appear to be too sparse when items are just one or two lines
	% long. Here we cancel the extra vertical spacing between list items.
	% The list margin is adjusted due to Chinese typesetting traditions.
	\RequirePackage{enumitem}
	\setlist{nolistsep, leftmargin = 1.5\parindent}
\fi

\ifthss@opt@spechap
	% This command is used to start a chapter without numbering, and correctly set
	% up the headers and footers in the chapter.
	\newcommand{\specialchap}[1]{%
		\chapter*{#1}\addcontentsline{toc}{chapter}{#1}
		\markboth{#1}{}\phantomsection%
	}
\fi

\AtBeginDocument{
	% Set up spacing for displayed formulae.
	\setlength{\abovedisplayskip}{\belowdisplayshortskip}
	\setlength{\belowdisplayskip}{\abovedisplayskip}

	\ifthss@opt@pdftoc
		% Add PDF bookmark for table of contents.
		\let\thss@tmp@tableofcontents\tableofcontents
		\renewcommand{\tableofcontents}{%
			\thss@int@pdfmark{\contentsname}{contents}
			\thss@tmp@tableofcontents%
		}
	\fi


}

% eg. `\thss@int@infoitema{ctitle}' will expand to:
%   \def\ctitle#1{\def\@ctitle{#1}}
%   \define@key{thss@info}{ctitle}{\ctitle{#1}}
\def\thss@int@infoitema#1{
	\@namedef{#1}##1{\@namedef{@#1}{##1}}
	\define@key{thss@info}{#1}{\@nameuse{#1}{##1}}
}
% eg. `\thss@int@infoitemb{cuniversity}' will expand to:
%   \define@key{thss@info}{cuniversity}{\def\cuniversity{#1}}
\def\thss@int@infoitemb#1{
	\define@key{thss@info}{#1}{\@namedef{#1}{##1}}
}
% Set up document information entries.
\thss@int@infoitema{ctitle}
\thss@int@infoitema{cauthor}
\thss@int@infoitema{studentid}
\thss@int@infoitema{date}
\thss@int@infoitema{school}
\thss@int@infoitema{cmajor}
\thss@int@infoitema{cmentor}
\thss@int@infoitema{ckeywords}
\thss@int@infoitema{blindid}
\thss@int@infoitema{discipline}
\thss@int@infoitemb{cuniversity}
\thss@int@infoitemb{cthesisname}
\thss@int@infoitemb{thesiscover}
\thss@int@infoitemb{cabstractname}
% Set up document information using the `key = value' grammar.
\newcommand*{\pkuthssinfo}[1]{\setkeys{thss@info}{#1}}

% Set up page layout.
\geometry{a4paper, 
	hmargin = 2.6cm,
	headheight = 1.5cm,
	headsep = 0.5cm,
	top = 3.0cm,
	bottom = 2.8cm,
	footskip = 0.75cm,
}

% Set up chapter/section/... captions.
% The `*skip' values are not supposed to be modified by the `ugly' option:
% the actual style of the school's guide and Word template seem to be different
% from the written specification (when applied verbatim in LaTeX), and here the
% actual style is used.
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{2}
\ctexset{
	chapter = {
		beforeskip = {6pt},
		afterskip = {18pt},
		nameformat = {},
		titleformat = {},
		format = {\zihao{3}\heiti\centering}
	},
	section = {
		beforeskip = {24pt},
		afterskip = {6pt},
		format = {\zihao{4}\heiti},
	},
	subsection = {
		beforeskip = {12pt},
		afterskip = {6pt},
		format = {\fontsize{13pt}{15.6bp}\selectfont\heiti},
	},
	subsubsection = {
		beforeskip = {12pt},
		afterskip = {6pt},
		format = {\zihao{-4}\heiti},
	}
}


% `\MakeUppercase' works problematically.
% eg. it converts `\cite{ctex}' into `\cite{CTEX}'.
% This option can disable `\MakeUppercase' in left/right heading marks.
\ifthss@opt@uppermark
	\def\thss@int@setcase#1{#1}
\else
	% Code copied from fancyhdr's `\nouppercase', with the redefinition of
	% `\uppercase' dropped to avoid disrupting CJKutf8.
	% cf. <https://code.google.com/p/ctex-kit/issues/detail?id=147>.
	\def\thss@int@setcase#1{%
		\let\MakeUppercase\relax%
		\expandafter\let\csname MakeUppercase \endcsname\relax%
		#1%
	}
\fi
% The actual page style setup.
\fancypagestyle{plain}{
	\fancyhf{}\renewcommand*{\headrulewidth}{0.75bp}
	\fancyfoot[C]{\zihao{5}\normalfont{\thepage}}
	\if@twoside
		\fancyhead[CE]{\zihao{5}\normalfont{\cuniversity\cthesisname}}
		\fancyhead[CO]{\zihao{5}\normalfont\thss@int@setcase{\leftmark}}
	\else
		\fancyhead[C]{\zihao{5}\normalfont\thss@int@setcase{\leftmark}}
	\fi
}
\pagestyle{plain}

% This places a bookmark pointing to somewhere near the page header;
% Result of simple `\chapter{...} \pdfbookmark{...}' does not look nice,
% because the bookmark will point to somewhere below the chapter mark.
\def\thss@int@pdfmark#1#2{%
	\if@openright\cleardoublepage\else\clearpage\fi
	\pdfbookmark[0]{#1}{#2}%
}

% Usage: \thss@int@fillinblank{(number of lines)}{(line width)}{(contents)}
\def\thss@int@fillinblank#1#2#3{%
	\makebox[0pt][l]{\parbox[t]{#2}{\centering{#3}}}\mbox{}%
	\parbox[t]{#2}{%
		\newcount\thss@tmp@linecount
		\thss@tmp@linecount=#1
		\loop\ifnum\thss@tmp@linecount>0
			% Fill specified space with underline on the bottom line. `\underline'
			% draws line on the baseline (not the bottom line), and this is why
			% `\uline' is used here instead.
			\ifnum\thss@tmp@linecount=1
				\uline{\makebox[#2]{}}
			\else
				\uline{\makebox[#2]{}}\\
			\fi
		\advance\thss@tmp@linecount by -1\relax
		\repeat%
	}%
}

% Set up format of the title page (cover).
\renewcommand{\maketitle}{%
	\thss@int@pdfmark{\titlepagename}{titlepage}
	% Make the title page centered.
	\begin{titlepage}\begingroup\centering
		% Emblem and inscription of the university, and type of thesis.
		{%
			\ifthss@opt@ugly%
				\zihao{-0}\includegraphics[height = 1.9em]{pkulogo}\hspace{0.3em}%
				\raisebox{0.32em}{\includegraphics[height = 1.3em]{pkuword}}\\[0.5em]
			\else%
				\zihao{1}\includegraphics[height = 2.4em]{pkulogo}\hspace{0.4em}%
				\raisebox{0.4em}{\includegraphics[height = 1.6em]{pkuword}}\\[0.8em]
			\fi%
			{\ifx\heiti\thesiscover\empty{\heiti\cthesisname}\else{\heiti\thesiscover}\fi}%
		}
		\vfill
		% Title of the thesis.
		{%
			\zihao{2}\linespread{1.6}\selectfont{\label@ctitle}%
			\thss@int@fillinblank{2}{0.64\textwidth}{\heiti{\zihao{1}\@ctitle}}%
		}
		\vfill
		% Information about the author.
		{%
			% Slightly adjust the line skip when using new font size.
			\zihao{3}\linespread{1.75}\selectfont
			\def\thss@tmp@len{0.56\textwidth}
			\begin{tabular}{l@{\extracolsep{0.2em}}c}
				{\bfseries\zihao{-3}\label@cauthor}		&
				\thss@int@fillinblank{1}{\thss@tmp@len}{\fangsong\@cauthor}		\\
				{\bfseries\zihao{-3}\label@studentid}	&
				\thss@int@fillinblank{1}{\thss@tmp@len}{\fangsong\@studentid}	\\
				{\bfseries\zihao{-3}\label@school}		&
				\thss@int@fillinblank{1}{\thss@tmp@len}{\fangsong\@school}		\\
				{\bfseries\zihao{-3}\label@cmentor}		&
				\thss@int@fillinblank{1}{\thss@tmp@len}{\fangsong\@cmentor}		\\
			\end{tabular}%
		}
		\vfill
		% Date.
		{\ifthss@opt@ugly\zihao{3}\else\zihao{-2}\fi\@date}
	\par\endgroup\end{titlepage}%
}

% Typeset the title page for double-blind review.
\newcommand{\makeblind}{%
	\thss@int@pdfmark{\titlepagename}{titlepage}
	\begin{titlepage}\begingroup
		\centering\zihao{3}\selectfont\fangsong\vspace*{0.5cm}
		{\zihao{-0}\heiti\cuniversity\cthesisname}\\[0.36\baselineskip]
		{\zihao{-2}\fangsong\label@blindcover}%
		\par\vspace{4\baselineskip}
		\renewcommand{\arraystretch}{1.25}
		\begin{tabular}{lp{0.75\textwidth}}
			\label@blindctitle	&	{\@ctitle}	\\
			\label@blinddiscipline	&	{\@discipline}	\\
			\label@blindid	&	{\@blindid}	\\
		\end{tabular}\par\vfill
		{\@date}\par\vspace*{0.5cm}
	\endgroup\end{titlepage}%
}

% Typeset the Chinese abstract.
\newenvironment{cabstract}{%
	\thss@int@pdfmark{\cabstractname}{cabstract}
	\chapter*{\cabstractname}\markboth{\cabstractname}{}%
}{% Keywords at the bottom of the page.
	\vfill\noindent\label@ckeywords{\@ckeywords}%
}

% Typeset the tableofcontents.
\renewcommand*{\tableofcontents}{%
    \chapter*{\contentsname}%
    \@mkboth{\MakeUppercase\contentsname}%
            {\MakeUppercase\contentsname}%
    \@starttoc{toc}%
}
\newcommand\thss@leaders{\titlerule*[4.4bp]{.}}
\newcommand\thss@set@toc@format{%
  \contentsmargin{\z@}%
  \titlecontents{chapter}
    [\z@]{\heiti}
    {\contentspush{\thecontentslabel\quad}}{}
    {\thss@leaders\thecontentspage}%
  \titlecontents{section}
    [1em]{}
    {\contentspush{\thecontentslabel\quad}}{}
    {\thss@leaders\thecontentspage}%
  \titlecontents{subsection}
    [2em]{}
    {\contentspush{\thecontentslabel\quad}}{}
    {\thss@leaders\thecontentspage}%
}

\thss@set@toc@format

\endinput
% vim:ft=tex:ts=2:sw=2
