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

    .inner {
        background: #444;
        padding-left: 20px;
        padding-right: 20px;
        min-width: 740px;
        max-width: 900px;
        margin: 0 auto;
    }
</style>

<body style="display: flex;margin:0;height: 100%;justify-content: center;">
    <div class="rpgui-content"
        style="height: 100%;width: 100%;overflow-y:scroll;display: flex;justify-content: center;align-items: center;">
        <div id="container" style="width: 100%;">
            <div id="main"></div>
            <div class="inner rpgui-container framed" style="position:relative">

                <header>
                    <h1 style="font-size:250%">Feedback Flux</h1>
                    <hr class="golden" />
                </header>

                <div style="display: flex;justify-content: center;">
                    <img src="{{asset("images/logo.jpg")}}" style="display:inline-block;" />
                </div>
                <form action="{{route('feedback.store')}}" method="POST">
                    @csrf
                    <div>
                        <textarea name="feedback" rows="20" style="margin-top:10px;font-size: 16px;"
                            placeholder="Submit Feedback"></textarea>
                    </div>

                    <div style="display: flex; justify-content: center;margin-top:10px;">
                        <button class="rpgui-button rpgui-cursor-default">Submit</button>
                    </div>
                </form>
                @session('message')
                    <div style="position:relative; margin-top: 20px;color: white;" class="rpgui-container framed-golden-2">
                        {{session('message')}}
                    </div>
                @endsession
            </div>
        </div>
    </div>
</body>

</html>