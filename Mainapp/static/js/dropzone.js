const uploadBox = document.querySelector('.upload_container');
const inputFile = document.querySelector('#uploadedFile');
const previewBox = document.getElementById('preview');
const uploadBtn = document.getElementById('uploaded-btn');

const word_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
const pdf_type = 'application/pdf'
const txt_type = 'text/plain'

// 박스 안에 Drag 들어왔을 때
uploadBox.addEventListener('dragenter', function(e) {
    // console.log('dragenter');
});

// 박스 안에 Drag 하고 있을 때
uploadBox.addEventListener('dragover', function(e) {
    e.preventDefault();
    // console.log('dragover');

    this.style.backgroundColor = '#4E4E4E';
});

// 박스 밖으로 Drag 나갈 때
uploadBox.addEventListener('dragleave', function(e) {
    // console.log('dragleave');

    this.style.backgroundColor = '#F4F4F4';
});

// 박스 안에서 Drag를 Drop했을 때
uploadBox.addEventListener('drop', function(e) {
    e.preventDefault();

    // console.log('drop');
    this.style.backgroundColor = '#F4F4F4';
    
    const data = e.dataTransfer;
    
    // 유효성 check
    if(!isValid(data)) return;

    inputFile.files = data.files;

    preview();
});

const handler = {
    init() {
        inputFile.addEventListener('change', () => {
            preview();
        });
    }
}

handler.init();

function checkExtension(fileName, fileSize) {
    var regex = new RegExp("(.*?)\.(exe|sh|zip|alz|xlsx)$");
    var maxSize = 5e+7;    // 50MB
    
    if (fileSize >= maxSize) {
    alert('50MB 이상인 파일은 업로드할 수 없습니다.');
    deleteImg();
    inputFile.value = null;
    return false;
    }

    if (regex.test(fileName)) {
        alert('업로드 불가능한 파일입니다.');
        deleteImg();
        inputFile.value = null;
        return false;
    }
    return true;
}


function isValid(data) {
    // 파일인지 유효성 검사
    if (data.types.indexOf('Files') < 0) {
        alert('업로드 불가능한 파일입니다.');
        deleteImg();
        return false;
    }
    
    // 파일의 사이즈는 50MB 미만
    if (data.files[0].size >= 1024 * 1024 * 50) {
        alert('50MB 이상인 파일은 업로드할 수 없습니다.');
        deleteImg();
        return false;
    }

    return true;
}

function preview() {
    // 또는, innerHTML 초기화
    while(previewBox.firstChild) {
        previewBox.removeChild(previewBox.firstChild);
    }

    previewBox.style.display = 'block';
    uploadBtn.style.display = 'none';
    
    var file = inputFile.files;

    if(!checkExtension(file[0].name, file[0].size)) {
        return false;
    }

    var fileName = file[0].name;

    var str = '<div style="width:100%; position: relative;">';
    str += '<span style="font-weight:bold; display:inline-block; width:710px;">'+fileName+'</span>';
    str += `<img src="/static/images/cancel.png" onClick="deleteImg()" style="float: right; margin-top: 5px; width: 30px; height: 30px; position: absolute; cursor: pointer;"/><br>`

    // 이미지 파일 미리보기
    if (file[0].type.match('image.*')) {
        var reader = new FileReader();    // 파일을 읽기 위한 FileReader 객체 생성
        reader.onload = function(e) {     // 파일 읽어들이기를 성공했을 때 호출되는 이벤트 핸들러
            str += `<img src="`+e.target.result+`" title="${fileName}" width=220 style="max-width:100%; height: auto; max-height:250px; margin-top:15px;" /></a>`;
            str += '</li></div>';
            previewBox.innerHTML += str;
        }
        reader.readAsDataURL(file[0]);
    }
    
    // word 파일
    else if (file[0].type.match(word_type)) {
        str += `<img src="/static/images/doc.png" title="${fileName}" width=220 style="max-width:100%; height: auto; max-height:250px; margin-top:15px;" /></a>`;
        previewBox.innerHTML += str;
    }

    // txt 파일
    else if (file[0].type.match(txt_type)) {
        str += `<img src="/static/images/txt.png" title="${fileName}" width=220 style="max-width:100%; height: auto; max-height:250px; margin-top:15px;" /></a>`;
        previewBox.innerHTML += str;
    }
    
    // pdf 파일
    else if (file[0].type.match(pdf_type)){
        str += `<img src="/static/images/pdf.png" id="img" title="${fileName}" data-pdf-thumbnail-file="/static/example.pdf" width=220 style="max-width:100%; height: auto; max-height:250px; margin-top:15px;" /></a>`;
        previewBox.innerHTML += str;

        // pdf 썸네일
        if (
            document.readyState === "complete" ||
            (document.readyState !== "loading" && !document.documentElement.doScroll)
        ) {
            createPDFThumbnails();
        } else {
            document.addEventListener("DOMContentLoaded", createPDFThumbnails);
        }   
    }
    
    // 나머지 파일
    else {
        alert('업로드 불가능한 파일입니다.');
        deleteImg();
    }
}

function deleteImg() {
    // 또는, innerHTML 초기화
    while(previewBox.firstChild) {
        previewBox.removeChild(previewBox.firstChild);
    }

    inputFile.value = null;

    previewBox.style.display = 'none';
    uploadBtn.style.display = 'inline-block';

    uploadBtn.style.margin = '140px auto';
}

/**
 * https://github.com/scandel/pdfThumbnails
 * Find all img elements with data-pdf-thumbnail-file attribute,
 * then load pdf file given in the attribute,
 * then use pdf.js to draw the first page on a canvas, 
 * then convert it to base64,
 * then set it as the img src.
 */
 var createPDFThumbnails = function(){
    var worker = null;
    var loaded = false;
    var renderQueue = [];

    // select all img elements with data-pdf-thumbnail-file attribute
    var nodesArray = Array.prototype.slice.call(document.querySelectorAll('img[data-pdf-thumbnail-file]'));

    if (!nodesArray.length) {
        // No PDF found, don't load PDF.js
        return;
    }

    if (!loaded && typeof(pdfjsLib) === 'undefined') {
        var src = document.querySelector('script[data-pdfjs-src]').getAttribute('data-pdfjs-src');

        // console.log(src);

        if (!src) {
            throw Error('PDF.js URL not set in "data-pdfjs-src" attribute: cannot load PDF.js');
        }

        var script = document.createElement('script'); 
        script.src = src;
        document.head.appendChild(script).onload = renderThumbnails;
        loaded = true;
    }
    else {
        renderThumbnails();
    }

    function renderThumbnails() {
        if (!pdfjsLib) {
            throw Error("pdf.js failed to load. Check data-pdfjs-src attribute.");
        }

        nodesArray.forEach(function(element) {
            if (null === worker) {
                worker = new pdfjsLib.PDFWorker();
            }

            let reader = new FileReader();
            reader.readAsDataURL(inputFile.files[0]);
            reader.onloadend = function(e, filePath) {
                var filePath = e.target.result;

                var imgWidth = element.getAttribute('width');
                var imgHeight = element.getAttribute('height');
    
                pdfjsLib.getDocument({url: filePath, worker: worker}).promise.then(function (pdf) {
                    pdf.getPage(1).then(function (page) {
                        var canvas = document.createElement("canvas");
                        var viewport = page.getViewport({scale: 1.0});
                        var context = canvas.getContext('2d');
    
                        if (imgWidth) {
                            viewport = page.getViewport({scale: imgWidth / viewport.width});
                        } else if (imgHeight) {
                            viewport = page.getViewport({scale: imgHeight / viewport.height});
                        }
    
                        canvas.height = viewport.height;
                        canvas.width = viewport.width;
    
                        page.render({
                            canvasContext: context,
                            viewport: viewport
                        }).promise.then(function () {
                            element.src = canvas.toDataURL();
                        });
                    }).catch(function() {
                        console.log("pdfThumbnails error: could not open page 1 of document " + filePath + ". Not a pdf ?");
                    });
                }).catch(function() {
                    console.log("pdfThumbnails error: could not find or open document " + filePath + ". Not a pdf ?");
                });
            }
        });
    }
};


