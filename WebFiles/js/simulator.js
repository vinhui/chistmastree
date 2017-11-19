$(document).ready(function() {
    var ledCount = 30;
    var run = false;
    var sequence = [];
    var currentStep = 0;

    var sequenceData = {
        ledStartID: 0,
        ledEndID: 0,
        red: 0,
        green: 0,
        blue: 0,
        delay: 10
    };

    createLedStrip();

    $(".row").on('click', '#run-sequence', function () {
        ledCount = parseInt($("input[name='led-count']").val());
        createLedStrip();
        sequence = parseSequence($("textarea[name='sequence-data']").val());
        runDelta = run;
        run = true;
        currentStep = 0;

        if (!runDelta)
            runSequence();
    });

    $(".row").on('click', '#stop-sequence', function () {
        run = false;

        setLedRangeColor(0, ledCount, 0, 0, 0);
    });

    function createLedStrip() {
        $(".strip-tester").html("");

        for (i = 0; i < ledCount; i++) {
            $(".strip-tester").append('<li class="list-inline-item pull-left" style="text-align: center; margin: 1px; padding-top: 3px; font-size: 8pt; width: 20px; height: 20px; background-color: black">' + i + '</li>');
        }
    }

    function parseSequence(data) {
        var output = [];
        var lines = data.split('\n');

        for (i = 0; i < lines.length; i++) {
            var line = lines[i].trim();

            if (line.slice(0, 1) != "#" && line != "") {
                var data = line.split(',');

                if (data.length == 6) {
                    var obj = Object.create(sequenceData);
                    obj.ledStartID = Math.max(parseInt(data[0]), 0);
                    obj.ledEndID = Math.min(parseInt(data[1]), ledCount);
                    obj.red = parseInt(data[2]);
                    obj.green = parseInt(data[3]);
                    obj.blue = parseInt(data[4]);
                    obj.delay = parseInt(data[5]);

                    output.push(obj);
                }
            }
        }

        return output;
    }

    function runSequence() {
        if (currentStep >= sequence.length)
            currentStep = 0;

        setTimeout(function () {
            if (run) {
                setLedRangeColor(
                    sequence[currentStep].ledStartID,
                    sequence[currentStep].ledEndID,
                    sequence[currentStep].red,
                    sequence[currentStep].green,
                    sequence[currentStep].blue);
                currentStep++;
                runSequence();
            }
        }, sequence[Math.max(currentStep - 1, 0)].delay);
    }

    function setLedRangeColor(start, end, r, g, b) {
        if (start == end) {
            setLedColor(start, r, g, b);
        }
        else {
            for (i = Math.max(Math.min(start, end), 0) ; i < Math.min(Math.max(start, end), ledCount) ; i++) {
                setLedColor(i, r, g, b);
            }
        }
    }

    function setLedColor(index, r, g, b) {
        $(".strip-tester li").eq(index).css("background-color", "rgb(" + r + "," + g + "," + b + ")");
    }
});