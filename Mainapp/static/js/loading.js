function loading() {
    $.LoadingOverlay("show", {
        // background       : "rgba(0, 0, 0, 0.5)",
        image            : "",
        maxSize          : 60,
        fontawesome      : "fa fa-spinner fa-pulse fa-fw",
        // fontawesomeColor : "#FFFFFF",
    });
}

function text_loading() {
    $.LoadingOverlay("show", {
        image       : "",
        text        : "Loading...",
        textAnimation : 'fadein',
    });
    setTimeout(function(){
        $.LoadingOverlay("text", '조금만 더 기다려주세요.');
    }, 5000);
    setTimeout(function(){
        $.LoadingOverlay("text", '조금만 더 기다려주세요...');
    }, 10000);
}