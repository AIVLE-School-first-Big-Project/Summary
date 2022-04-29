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

    var data0 = e.dataTransfer.files[0];
    console.dir(data0);
    console.log(data0.name);
    
    const data = e.dataTransfer;
    
    // 유효성 check
    if(!isValid(data)) return;
    
    const csrftoken = getCookie('csrftoken');

    const filePath = 'Uploaded Files/'+data.files[0].name;
    const replaceText = filePath.replace(/ /g, '_');

    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrftoken);
    // formData.append('fileTitle', data.files[0].name);
    // formData.append('uploadedFile', replaceText);

    formData.append('file', data.files[0]);
    
    console.log(replaceText);

    const ajax = fetch('/summary/ajax/', {
        method: 'post',
        body: formData
    });

    ajax.then(function(response) {
        return response.text();
    }).then(function(result) {
        console.log(result);
    });

    // document.getElementById('uploadedFile').value = data.files[0];
    // const value = document.getElementById('uploadedFile').value;
    // console.log(value);
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0 ; i < cookies.length ; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
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

function ajax(obj) {
    const xhr = new XMLHttpRequest();

    var method = obj.method || 'GET';
    var url = obj.url || '';
    var data = obj.data || null;

    /* 성공/에러 */
    xhr.addEventListener('load', function() {
        const data = xhr.responseText;

        if(obj.load)
            obj.load(data);
    });
    
    /* 성공 */
    xhr.addEventListener('loadend', function() {
        const data = xhr.responseText;

        if(obj.loadend)
            obj.loadend(data);
    });

    /* 실패 */
    xhr.addEventListener('error', function() {
        console.log('Ajax 중 에러 발생 : ' + xhr.status + ' / ' + xhr.statusText);

        if(obj.error) {
            obj.error(xhr, xhr.status, xhr.statusText)
        }
    });

    /* 중단 */
    xhr.addEventListener('abort', function() {
        if(obj.abort) {
            obj.abort(xhr);
        }
    });

    /* 진행 */
    xhr.upload.addEventListener('progress', function() {
        if(obj.progress) {
            obj.progress(xhr);
        }
    });

    /* 요청 시작 */
    xhr.addEventListener('loadstart', function() {
        if(obj.loadstart)
            obj.loadstart(xhr);
    });

    if(obj.async === false)
        xhr.open(method, url, obj.async);
    else
        xhr.open(method, url, true);
    
    if(obj.contentType)
        xhr.setRequestHeader('Content-Type', obj.contentType);
    
    xhr.send(data);
}