<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Feedback Flux</title>
    <link href='https://fonts.googleapis.com/css?family=Chivo:900' rel='stylesheet' type='text/css'>

    <link rel="stylesheet" type="text/css" href="{{asset('css/rpgui.css')}}">
    <script src="{{asset('js/rpgui.css')}}"></script>
</head>
<style>
    body,
    #container {
        background: #222;
        padding-top: 20px;
        padding-bottom: 20px;
    }

    .product-description {
        text-align: center;
        overflow: hidden;
        text-overflow: ellipsis;
        height: 100px;
        margin-bottom: 10px;
    }

    .inner {
        background: #444;
        padding-left: 20px;
        padding-right: 20px;
        margin: 0 auto;
    }
</style>

<body style="margin:0;height: 100%;width: 100%;">
    <div class="rpgui-content" style="height: 100%;width: 100%;overflow-y:scroll;">
        <div id="container " style="padding: 20px;">
            <div id="main"></div>
            <div class="inner rpgui-container framed" style="position:relative">

                <header>
                    <div style="display: flex;justify-content: space-between;">
                        <h1 style="font-size: large;">All Submitted Feedback</h1>

                    </div>

                    <hr class="golden" />
                </header>


                <div id="product-container" >
                    @foreach ($feedbacks as $feedback)
                        <div class="rpgui-container framed-golden-2" style="position:relative; padding: 10px;margin: 10px;color: white;">
                            {!! $feedback->feedback !!}

                        </div>
                    @endforeach

                </div>
            </div>
        </div>
    </div>




</body>

</html>


<!-- <!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Laravel</title>

        <link rel="preconnect" href="https://fonts.bunny.net">
        <link href="https://fonts.bunny.net/css?family=figtree:400,600&display=swap" rel="stylesheet" />
    </head>
    <body class="font-sans antialiased dark:bg-black dark:text-white/50">
        @foreach ($feedbacks as $feedback)
            {!! $feedback->feedback !!}
        @endforeach
    </body>
</html> -->