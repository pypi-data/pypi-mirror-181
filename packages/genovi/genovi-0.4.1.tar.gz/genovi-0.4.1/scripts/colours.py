# GenoVi is a pipeline that generates circular maps for bacterial (complete or non-complete)
# genomes using Circos software. It also allows the user to annotate COG classifications
# through DeepNOG predictions.
# 
# GenoVi is under a BY-NC-SA Creative Commons License, Please cite. Cumsille et al., 2021
# You may remix, tweak, and build upon this work even for commercial purposes, as long as
# you credit this work and license your new creations under the identical terms.
# 
# Developed by Andres Cumsille, Andrea Rodriguez, Roberto E. Duran & Vicente Saona Urmeneta
# For any code related query, contact: andrea.rodriguezdelherbe@rdm.ox.ac.uk, vicente.saona@sansano.usm.cl

import re

__all__ = ['parseColours']

# This function is for parsing colour schemes
def parseColours(colour_scheme = "auto", background_colour = "none", GC_content = "auto", GC_skew ='auto', tRNA = 'auto', rRNA = 'auto', CDS_positive = 'auto', CDS_negative = 'auto', skew_line_colour = '0, 0, 0'):
    colour_scheme = colour_scheme.lower()
    # if re.match("^\s*[012]?\d?\d\s*,\s*[012]?\d?\d\s*,\s*[012]?\d?\d\s*$", background_colour):
    #     background_colour = "rgb(" + background_colour + ")"
    gc_skew_original_argument = re.match("^\s*(?P<red1>[012]?\d?\d)\s*,\s*(?P<green1>[012]?\d?\d)\s*,\s*(?P<blue1>[012]?\d?\d)\s*[,;-]\s*(?P<red2>[012]?\d?\d)\s*,\s*(?P<green2>[012]?\d?\d)\s*,\s*(?P<blue2>[012]?\d?\d)\s*$", GC_skew)
    if gc_skew_original_argument:
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,{},{}),remap_int(var(value),0,0,{},{}),remap_int(var(value),0,0,{},{})))'.format(
            gc_skew_original_argument.group("red1"),
            gc_skew_original_argument.group("red2"),
            gc_skew_original_argument.group("green1"),
            gc_skew_original_argument.group("green2"),
            gc_skew_original_argument.group("blue1"),
            gc_skew_original_argument.group("blue2"))
    
    if colour_scheme == "blue" or colour_scheme == "blues":
        GC_content = "14, 29, 130" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("rdbu-7-div-%d",remap_int(var(value),0,0,7,5)))' if GC_skew == "auto" else GC_skew
        tRNA = "99, 103, 186" if tRNA == "auto" else tRNA
        rRNA = "89, 123, 186" if rRNA == "auto" else rRNA
        CDS_positive = "191, 204, 217" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "171, 178, 217" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "163, 191, 217" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "paradise" or colour_scheme == "tropical":
        GC_content = "246,232,195" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("brbg-11-div-%d",remap_int(var(value),0,0,0,1)))' if GC_skew == "auto" else GC_skew
        tRNA = "140,81,10" if tRNA == "auto" else tRNA
        rRNA = "223,194,125" if rRNA == "auto" else rRNA
        CDS_positive = "1,102,94" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "128,205,193" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "163, 163, 217" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "blossom" or colour_scheme == "cherry" or colour_scheme == "sakura":
        GC_content = "230,245,208" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("piyg-11-div-%d",remap_int(var(value),0,0,11,10)))' if GC_skew == "auto" else GC_skew
        tRNA = "241,182,218" if tRNA == "auto" else tRNA
        rRNA = "184,225,134" if rRNA == "auto" else rRNA
        CDS_positive = "142,1,82" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "222,119,174" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "163, 163, 217" if skew_line_colour == "auto" else skew_line_colour    
    elif colour_scheme == "dawn" or colour_scheme == "sunrise":
        GC_content = "0,0,0" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,230,213),remap_int(var(value),0,0,159,94),remap_int(var(value),0,0,0,0)))' if GC_skew == "auto" else GC_skew
        tRNA = "240, 228, 66" if tRNA == "auto" else tRNA
        rRNA = "0, 158, 115" if rRNA == "auto" else rRNA
        CDS_positive = "204, 121, 167" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "0, 114, 178" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "163, 163, 217" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "autumn" or colour_scheme == "fall":  # Color Universal Design, Suggested by Okabe, Ito, in "Color Universal Design (CUD) - How to make figures and presentations that are friendly to Colorblind people", available at https://jfly.uni-koeln.de/color/
        GC_content = "0,0,0" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,0,240),remap_int(var(value),0,0,158,228),remap_int(var(value),0,0,115,66)))' if GC_skew == "auto" else GC_skew
        tRNA = "204, 121, 167" if tRNA == "auto" else tRNA
        rRNA = "86, 180, 233" if rRNA == "auto" else rRNA
        CDS_positive = "213, 94, 0" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "230, 159, 0" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "163, 163, 217" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "purple" or colour_scheme == "purples":
        GC_content = "57, 1, 120" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("puor-7-div-%d",remap_int(var(value),0,0,7,6)))' if GC_skew == "auto" else GC_skew
        tRNA = "108, 95, 156" if tRNA == "auto" else tRNA
        rRNA = "128, 85, 156" if rRNA == "auto" else rRNA
        CDS_positive = "196, 187, 237" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "151, 143, 191" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "163, 163, 217" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "soil":
        GC_content = "89, 60, 6" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("brbg-7-div-%d",remap_int(var(value),0,0,7,5)))' if GC_skew == "auto" else GC_skew
        tRNA = "0, 112, 11" if tRNA == "auto" else tRNA
        rRNA = "20, 112, 1" if rRNA == "auto" else rRNA
        CDS_positive = "185, 199, 186" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "175, 201, 178" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "89, 194, 115" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "greyscale" or colour_scheme == "grayscale" or colour_scheme == "grey" or colour_scheme == "gray":
        GC_content = "87, 87, 87" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("rdgy-7-div-%d",remap_int(var(value),0,0,7,5)))' if GC_skew == "auto" else GC_skew
        tRNA = "115, 115, 115" if tRNA == "auto" else tRNA
        rRNA = "115, 115, 115" if rRNA == "auto" else rRNA
        CDS_positive = "209, 209, 209" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "184, 184, 184" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "171, 171, 171" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "velvet" or colour_scheme == "pink" or colour_scheme == "red":
        GC_content = "82, 1, 30" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("purd-7-seq-%d",remap_int(var(value),0,0,7,4)))' if GC_skew == "auto" else GC_skew
        tRNA = "130, 1, 49" if tRNA == "auto" else tRNA
        rRNA = "130, 21, 69" if rRNA == "auto" else rRNA
        CDS_positive = "217, 195, 205" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "196, 187, 193" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "230, 200, 211" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "pastel":
        GC_content = "196, 227, 255" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("pastel1-7-qual-%d",remap_int(var(value),0,0,4,3)))' if GC_skew == "auto" else GC_skew
        tRNA = "143, 143, 143" if tRNA == "auto" else tRNA
        rRNA = "143, 143, 143" if rRNA == "auto" else rRNA
        CDS_positive = "255, 222, 235" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "181, 255, 214" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "150, 150, 150" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "ocean" or colour_scheme == "sea":
        GC_content = "24,138,141" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,127",remap_int(var(value),0,0,23,63),remap_int(var(value),0,0,87,159)))' if GC_skew == "auto" else GC_skew
        tRNA = "0, 83, 83" if tRNA == "auto" else tRNA
        rRNA = "0, 83, 83" if rRNA == "auto" else rRNA
        CDS_positive = "96,221,142" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "23,87,126" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "24,138,141" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "wood":
        GC_content = "150,90,49" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,120,163),remap_int(var(value),0,0,118,124),remap_int(var(value),0,0,37,81)))' if GC_skew == "auto" else GC_skew
        tRNA = "131,62,32" if tRNA == "auto" else tRNA
        rRNA = "62,131,32" if rRNA == "auto" else rRNA
        CDS_positive = "73,115,54" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "185,157,103" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "143,76,40" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "beach":
        GC_content = "231,207,133" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,93,210),remap_int(var(value),0,0,204,173),remap_int(var(value),0,0,167,128)))' if GC_skew == "auto" else GC_skew
        tRNA = "184,141,117" if tRNA == "auto" else tRNA
        rRNA = "117,167,184" if rRNA == "auto" else rRNA
        CDS_positive = "131,246,191" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "79,176,159" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "93,204,167" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "desert":
        GC_content = "225,168,111" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,237,193),remap_int(var(value),0,0,242,98),remap_int(var(value),0,0,154,2)))' if GC_skew == "auto" else GC_skew
        tRNA = "36,16,16" if tRNA == "auto" else tRNA
        rRNA = "180,165,150" if rRNA == "auto" else rRNA
        CDS_positive = "240,198,70" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "237,242,154" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "225,168,111" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "ice" or colour_scheme == "frozen":
        GC_content = "186,242,239" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,37,162),remap_int(var(value),0,0,124,210),remap_int(var(value),0,0,163,223)))' if GC_skew == "auto" else GC_skew
        tRNA = "57,109,124" if tRNA == "auto" else tRNA
        rRNA = "97,129,144" if rRNA == "auto" else rRNA
        CDS_positive = "120,143,255" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "200,223,235" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "162,210,223" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "island":
        GC_content = "75,157,19" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,78,245),remap_int(var(value),0,0,247,229),remap_int(var(value),0,0,171,147)))' if GC_skew == "auto" else GC_skew
        tRNA = "75,157,19" if tRNA == "auto" else tRNA
        rRNA = "180,165,150" if rRNA == "auto" else rRNA
        CDS_positive = "254,155,227" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "154,215,173" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "155,187,89" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "forest":
        GC_content = "45,158,48" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,32,136),remap_int(var(value),0,0,103,208),remap_int(var(value),0,0,78,95)))' if GC_skew == "auto" else GC_skew
        tRNA = "109,137,75" if tRNA == "auto" else tRNA
        rRNA = "104,37,11" if rRNA == "auto" else rRNA
        CDS_positive = "136,208,95" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "105,184,128" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "45,158,48" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "toxic":
        GC_content = "137,4,177" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,106,11),remap_int(var(value),0,0,8,97),remap_int(var(value),0,0,136,11)))' if GC_skew == "auto" else GC_skew
        tRNA = "0,0,0" if tRNA == "auto" else tRNA
        rRNA = "50,50,50" if rRNA == "auto" else rRNA
        CDS_positive = "1,223,1" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "237,4,177" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "137,4,177" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "fire":
        GC_content = "216,0,0" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,0",remap_int(var(value),0,0,216,242),remap_int(var(value),0,0,0,85)))' if GC_skew == "auto" else GC_skew
        tRNA = "140,40,0" if tRNA == "auto" else tRNA
        rRNA = "161,0,0" if rRNA == "auto" else rRNA
        CDS_positive = "255,129,0" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "242,85,0" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "234,35,0" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "spring":
        GC_content = "249,150,174" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,217,107),remap_int(var(value),0,0,182,206),remap_int(var(value),0,0,253,238)))' if GC_skew == "auto" else GC_skew
        tRNA = "137,4,177" if tRNA == "auto" else tRNA
        rRNA = "237,164,207" if rRNA == "auto" else rRNA
        CDS_positive = "186,240,163" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "246,240,163" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "159,244,223" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "electric":
        GC_content = "22,48,190" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,255,160),remap_int(var(value),0,0,255,220),remap_int(var(value),0,0,0,205)))' if GC_skew == "auto" else GC_skew
        tRNA = "130,130,140" if tRNA == "auto" else tRNA
        rRNA = "2,4,100" if rRNA == "auto" else rRNA
        CDS_positive = "220,220,230" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "255,255,155" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "159,244,223" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "stone":
        GC_content = 'eval(sprintf("hsv(200,0.38,0.%d)", 56+rand(10)))' if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,159,45),remap_int(var(value),0,0,181,39),remap_int(var(value),0,0,184,39)))' if GC_skew == "auto" else GC_skew
        tRNA = "60,48,48" if tRNA == "auto" else tRNA
        rRNA = "45,39,39" if rRNA == "auto" else rRNA
        CDS_positive = "159,181,184" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "184,169,159" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "100,100,100" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "skin":
        GC_content = '224,172,105' if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,241,141),remap_int(var(value),0,0,194,85),remap_int(var(value),0,0,125,36)))' if GC_skew == "auto" else GC_skew
        tRNA = "141,85,36" if tRNA == "auto" else tRNA
        rRNA = "141,95,66" if rRNA == "auto" else rRNA
        CDS_positive = "255,219,172" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "241,194,125" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "224,172,105" if skew_line_colour == "auto" else skew_line_colour
    elif colour_scheme == "neutral":
        GC_content = "94, 120, 145" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("bupu-7-seq-%d",remap_int(var(value),0,0,4,3)))' if GC_skew == "auto" else GC_skew
        tRNA = "67, 14, 110" if tRNA == "auto" else tRNA
        rRNA = "67, 110, 14" if rRNA == "auto" else rRNA
        CDS_positive = "186, 186, 186" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "140, 140, 140" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "171, 171, 171" if skew_line_colour == "auto" else skew_line_colour
    else: # if colour_scheme == "strong" # Color-blind friendly palette
        GC_content = "0, 158, 115" if GC_content == "auto" else GC_content
        GC_skew = 'eval(sprintf("%d,%d,%d",remap_int(var(value),0,0,213,0),remap_int(var(value),0,0,94,0),remap_int(var(value),0,0,0,0)))' if GC_skew == "auto" else GC_skew
        tRNA = "230, 159, 0" if tRNA == "auto" else tRNA
        rRNA = "204, 121, 167" if rRNA == "auto" else rRNA
        CDS_positive = "86, 180, 233" if CDS_positive == "auto" else CDS_positive
        CDS_negative = "0, 114, 178" if CDS_negative == "auto" else CDS_negative
        skew_line_colour = "163, 163, 217" if skew_line_colour == "auto" else skew_line_colour

    return colour_scheme, background_colour, GC_content, GC_skew, tRNA, rRNA, CDS_positive, CDS_negative, skew_line_colour
