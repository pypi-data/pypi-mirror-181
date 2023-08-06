var myBuiltIn = [{% for command in commands %} "{{ command }}", {% endfor %}];
var vsKeywords = ["VERSION", "Xponge", "Visual Sponge"];