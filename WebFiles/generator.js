$("#generate-button").click(function(){
    generateFade();
    $("#generate-output").effect("highlight");
});
function remGradientColor() {
    $(".generate-color:last").parent().remove();
    $(".generate-color-rem:last").show();
    $(".generate-color-add:last").show();
}
function addGradientColor() {
    $(".generate-color-rem").hide();
    $(".generate-color-add").hide();
    var index = $(".generate-color").length + 1;
    $(".generate-color:last").parent().after(`
                    <div class="row">
                        <label for="generate-color-`+index+`" class="col-sm-2">Color #`+index+`</label>
                        <input type="color" class="col-sm-2 generate-color" id="generate-color-`+index+`" value="#000000"/>
                        <button class="col-sm-1 generate-color-rem">-</button>
                        <button class="col-sm-1 generate-color-add">+</button>
                    </div>`);
}
$(document).on('click', '.generate-color-add', function () {
    addGradientColor();
});
$(document).on('click', '.generate-color-rem', function () {
    remGradientColor();
});
function generateFade() {
    var startLed = parseInt($("#generate-startled").val());
    var endLed = parseInt($("#generate-endled").val());
    var duration = parseInt($("#generate-duration").val());
    var step = parseInt($("#generate-step").val());
    var colors = $(".generate-color").map(function() { return $(this).val() });

    var output = "";

    var section = duration / (colors.length - 1);
    for (var n = 0; n < colors.length - 1; n++) {
        for (var i = 0; i < section; i += step) {
            var t = i / section;
            var color = lerpColor(colors[n], colors[n + 1], t);
            var rgb = hexToRgb(color);
            output += startLed+","+endLed+","+rgb[0]+","+rgb[1]+","+rgb[2]+","+step+"\n";
        }
    }

   var endrgb = hexToRgb(colors[colors.length - 1]);
   output += startLed+","+endLed+","+endrgb[0]+","+endrgb[1]+","+endrgb[2]+","+step;
   $("#generate-output").val(output);
}

// https://gist.github.com/rosszurowski/67f04465c424a9bc0dae
function lerpColor(a, b, amount) { 
    var ah = parseInt(a.replace(/#/g, ''), 16),
        ar = ah >> 16, ag = ah >> 8 & 0xff, ab = ah & 0xff,
        bh = parseInt(b.replace(/#/g, ''), 16),
        br = bh >> 16, bg = bh >> 8 & 0xff, bb = bh & 0xff,
        rr = ar + amount * (br - ar),
        rg = ag + amount * (bg - ag),
        rb = ab + amount * (bb - ab);

    return '#' + ((1 << 24) + (rr << 16) + (rg << 8) + rb | 0).toString(16).slice(1);
}

// https://stackoverflow.com/questions/21646738/convert-hex-to-rgba
function hexToRgb(hex) {
    var c;
    if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
        c = hex.substring(1).split('');
        if(c.length== 3){
            c= [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c= '0x'+c.join('');
        return [(c>>16)&255, (c>>8)&255, c&255];
    }
    throw new Error('Bad Hex');
}