var div9 = document.querySelector('#layoutSidenav_content');
var btnUpload = div9.querySelector('.main-button-black');
var inputFile = div9.querySelector('input[type="file"]');
var uploadBox = div9.querySelector('.upload_container')

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

    console.dir(e.dataTransfer);

    var data = e.dataTransfer.files[0];
    console.dir(data);
});

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

function ajax(obj) {
    const xhr = new XMLHttpRequest();

    
}