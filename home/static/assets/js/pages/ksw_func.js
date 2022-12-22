    // 로딩창 키는 함수
    function openLoading() {
        //화면 높이와 너비를 구합니다.
        let maskHeight = $(document).height();
        let maskWidth = window.document.body.clientWidth;
        //출력할 마스크를 설정해준다.

        let mask = "<div id='mask' style='position:absolute; z-index:9000; background-color:#000000; display:none; left:0; top:0;'></div>";
        // 로딩 이미지 주소 및 옵션
        let loadingImg = '';

        //loadingImg += "<div id='loadingImg' style='position:absolute; top: calc(50% - (600px / 2)); width:100%; z-index:99999999;'>";
        //loadingImg += " <img src='https://loadingapng.com/animation.php?image=4&fore_color=000000&back_color=FFFFFF&size=128x128&transparency=1&image_type=0&uncacher=75.5975991029623' style='position: relative; display: block; margin: 0px auto;'/>";
        //loadingImg += "</div>"; 

        loadingImg += "<div class='spinner-border text-light' id='loadingImg' role='status' style='position:absolute; top: calc(46% - (600px / 2)); left: calc(46%); z-index:99999999;'>";
        loadingImg += " <span class='sr-only'>Loading...</span>";
        loadingImg += "</div>";
        //레이어 추가

        $('body')
            .append(mask)
            .append(loadingImg)
        //마스크의 높이와 너비로 전체 화면을 채운다.
        $('#mask').css({
            'width': maskWidth,
            'height': maskHeight,
            'opacity': '0.3'
        });
        //마스크 표시
        $('#mask').show();
        //로딩 이미지 표시
        $('#loadingImg').show();
    }

    // 로딩창 끄는 함수
    function closeLoading() {
        $('#mask, #loadingImg').hide();
        $('#mask, #loadingImg').empty();
    }


    function layer_popup(el){

        var $el = $(el);    //레이어의 id를 $el 변수에 저장
        var isDim = $el.prev().hasClass('dimBg'); //dimmed 레이어를 감지하기 위한 boolean 변수

        console.log(el)

        isDim ? $('.dim-layer').fadeIn() : $el.fadeIn();

        var $elWidth = ~~($el.outerWidth()),
            $elHeight = ~~($el.outerHeight()),
            docWidth = $(document).width(),
            docHeight = $(document).height();

        // 화면의 중앙에 레이어를 띄운다.
        if ($elHeight < docHeight || $elWidth < docWidth) {
            $el.css({
                marginTop: -327,
                marginLeft: -516
            })
        } else {
            $el.css({top: 0, left: 0});
        }

        $el.find('a.btn-layerClose').click(function(){
            isDim ? $('.dim-layer').fadeOut() : $el.fadeOut(); // 닫기 버튼을 클릭하면 레이어가 닫힌다.

            $('html, body').css({'overflow': 'auto', 'height': '100%'}); //scroll hidden 해제
            $('#element').off('scroll touchmove mousewheel'); // 터치무브 및 마우스휠 스크롤 가능

            return false;
        });

        $('.layer .dimBg').click(function(){
            $('.dim-layer').fadeOut();
            return false;
        });

        $('html, body').css({'overflow': 'hidden', 'height': '100%'}); // 모달팝업 중 html,body의 scroll을 hidden시킴
        $('#element').on('scroll touchmove mousewheel', function(event) { // 터치무브와 마우스휠 스크롤 방지
            event.preventDefault();
            event.stopPropagation();

            return false;
        });

    }