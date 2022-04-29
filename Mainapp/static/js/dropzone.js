const uploadBox = document.querySelector('.upload_container');
const inputFile = document.querySelector('#uploadedFile');
const previewBox = document.getElementById('preview');
const uploadBtn = document.getElementById('uploaded-btn');
console.dir(inputFile);

// 박스 안에 Drag 들어왔을 때
uploadBox.addEventListener('dragenter', function(e) {
    console.log('dragenter');
});

// 박스 안에 Drag 하고 있을 때
uploadBox.addEventListener('dragover', function(e) {
    e.preventDefault();
    console.log('dragover');

    this.style.backgroundColor = '#4E4E4E';
});

// 박스 밖으로 Drag 나갈 때
uploadBox.addEventListener('dragleave', function(e) {
    console.log('dragleave');

    this.style.backgroundColor = '#F4F4F4';
});

// 박스 안에서 Drag를 Drop했을 때
uploadBox.addEventListener('drop', function(e) {
    e.preventDefault();

    console.log('drop');
    this.style.backgroundColor = '#F4F4F4';
    
    const data = e.dataTransfer;
    
    // 유효성 check
    if(!isValid(data)) return;

    inputFile.files = data.files;
    console.dir(inputFile);

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
    var regex = new RegExp("(.*?)\.(exe|sh|zip|alz)$");
    var maxSize = 5e+7;    // 50MB
    
    if (fileSize >= maxSize) {
    alert('파일 사이즈 초과');
    inputFile.value = null;
    return false;
    }

    if (regex.test(fileName)) {
        alert('업로드 불가능한 파일이 있습니다.');
        inputFile.value = null;
        return false;
    }
    return true;
}


function isValid(data) {
    // 파일인지 유효성 검사
    if (data.types.indexOf('Files') < 0)
        return false;
    
    // 파일의 사이즈는 50MB 미만
    if (data.files[0].size >= 1024 * 1024 * 50) {
        alert('50MB 이상인 파일은 업로드할 수 없습니다.');
        return false;
    }

    return true;
}

function preview() {
    // 또는, innerHTML 초기화
    while(previewBox.firstChild) {
        previewBox.removeChild(previewBox.firstChild);
    }

    previewBox.style.visibility = 'visible';
    uploadBtn.style.visibility = 'hidden';
    
    var file = inputFile.files;

    if(!checkExtension(file[0].name, file[0].size)) {
        return false;
    }

    var fileName = file[0].name;

    var str = '<div>';
    str += '<span>'+fileName+'</span><br>';

    // 이미지 파일 미리보기
    if (file[0].type.match('image.*')) {
        // var reader = new FileReader();    // 파일을 읽기 위한 FileReader 객체 생성
        // reader.onload = function(e) {     // 파일 읽어들이기를 성공했을 때 호출되는 이벤트 핸들러
        //     str += '<img src="'+e.target.result+'" title="'+fileName+'" width=100 height=100 />';
        //     str += '</li></div>';
        //     previewBox.innerHTML += str;
        // }
        // reader.readAsDataURL(f);
    } else {
        str += `<img src="/static/images/pdf.png" title="${fileName}" width=100 height=100 />`;
        previewBox.innerHTML += str;
    }                       
}