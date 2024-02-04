var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
});

function showToast(message, type) {
    const toast = new bootstrap.Toast(document.getElementById('alert-toast'));
    document.getElementById("alert_header").classList.add("bg-" + type);
    document.getElementById("alert_header").classList.add("text-light");

    document.querySelector('.toast-body').textContent = message;
    toast.show();
    setTimeout(() => {
        toast.hide();
    }, 5000);
}

window.addEventListener("pageshow", function (event) {
    if (localStorage.getItem('reload') === 'true') {
        localStorage.removeItem('reload');
        console.log("aghaaaa");
        setTimeout(() => {
            {
                location.reload();
            }
        }, 500);
        location.reload();
    }
    if (localStorage.getItem('message') === 'true') {
        showToast(localStorage.getItem('message_text'), localStorage.getItem('message_type'));
        localStorage.removeItem('message');
        localStorage.removeItem('message_text');
        localStorage.removeItem('message_type');
    }
});

function changeIcon() {
    // یافتن عنصر آیکون با کلاس addToWish
    var icon = document.querySelector(".addToWish i");
    // یافتن عنصر لیست با کلاس addToWish
    var list = document.querySelector(".addToWish");
    // یافتن شیء tooltip مربوط به عنصر لیست
    var tooltip = bootstrap.Tooltip.getInstance(list);
    // بررسی کلاس های آیکون
    if (icon.classList.contains("bi-heart-fill")) {
        // اگر آیکون قلب پر باشد، آن را به قلب خالی تغییر دهید
        icon.classList.remove("bi-heart-fill");
        icon.classList.add("bi-heart");
        // تغییر متن tooltip به "افزودن به علاقه مندی"
        tooltip.hide();
        list.setAttribute("data-bs-original-title", "افزودن به علاقه مندی");
        list.setAttribute("title", "افزودن به علاقه مندی");
        tooltip.show();
    } else {
        // اگر آیکون قلب خالی باشد، آن را به قلب پر تغییر دهید
        icon.classList.remove("bi-heart");
        icon.classList.add("bi-heart-fill");
        // تغییر متن tooltip به "حذف از علاقه مندی"
        tooltip.hide();
        list.setAttribute("data-bs-original-title", "حذف از علاقه مندی");
        list.setAttribute("title", "حذف از علاقه مندی");
        tooltip.show();
    }
}


// <!-- تعریف یک آیکون قلب با قابلیت افزودن به علاقه مندی ها -->
// <li class="d-inline-block"
//     data-bs-toggle="tooltip"
//     data-bs-placement="top"
//     title="افزودن به علاقه مندی">
//     <!-- اضافه کردن رویداد onclick به عنصر a -->
//     <a href="#" class="addToWish d-inline-block rounded" onclick="changeIcon()">
//         <!-- استفاده از آیکون fontawesome -->
//         <i class="fa fa-heart"></i>
//     </a>
// </li>


jQuery('.slider-item').owlCarousel({
    loop: true,
    margin: 10,
    rtl: true,
    nav: false,
    dots: true,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
        },
        600: {
            items: 2,
        },
        1000: {
            items: 2,
        }
    }
});

// jQuery('footer span.scrooltop').click(function (){
//     jQuery('body,html').animate((screenTop 0),2000)
// });

// let mybutton = document.getElementsByClassName(scrooltop);
// window.onscroll=function (){scrollFunction()};
// function scrollFunction(){
//     if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20){
//         mybutton.style.display="block";
//     }
//     else {
//         mybutton.style.display="none";
//     }
// }
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

jQuery('.cat-slider-item').owlCarousel({
    loop: false,
    rewind: true,
    margin: 10,
    rtl: true,
    nav: false,
    dots: true,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
        },
        600: {
            items: 3,
        },
        1000: {
            items: 4,
        }
    }
});

jQuery('.product-gallery').owlCarousel({
    loop: true,
    margin: 50,
    rtl: true,
    nav: false,
    dots: true,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
        },
        600: {
            items: 3,
        },
        1000: {
            items: 4,
        }
    }
});

jQuery('.timer').startTimer();

// $("#appzoon").elevateZoom();

// jQuery("#appzoon").elevateZoom({
//     zoomType: "inner",
//     cursor: "crossshair"
// });

// jQuery('[data-fancybox="gallery"]').fancybox({})

function iranwebsv(state) {
    with (document.getElementById('city')) {
        options.length = 0;

        if (state == 0) {
            options[0] = new Option('لطفا استان را انتخاب نمایید', '0');
        }

        if (state == 1) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('احمدآبادمستوفي', '33131');
            options[2] = new Option('ادران', '31541');
            options[3] = new Option('اسلام آباد', '18641');
            options[4] = new Option('اسلام شهر', '331');
            options[5] = new Option('اكبرآباد', '37671');
            options[6] = new Option('اميريه', '39861');
            options[7] = new Option('انديشه', '31686');
            options[8] = new Option('اوشان', '33431');
            options[9] = new Option('آبسرد', '39761');
            options[10] = new Option('آبعلي', '39741');
            options[11] = new Option('باغستان', '33541');
            options[12] = new Option('باقر شهر', '18131');
            options[13] = new Option('برغان', '33631');
            options[14] = new Option('بومهن', '16551');
            options[15] = new Option('پارچين', '33971');
            options[16] = new Option('پاكدشت', '3391');
            options[17] = new Option('پرديس', '16581');
            options[18] = new Option('پرند', '37611');
            options[19] = new Option('پس قلعه', '19731');
            options[20] = new Option('پيشوا', '3381');
            options[21] = new Option('تجزيه مبادلات لشكر  ', '1012');
            options[22] = new Option('تهران', '1');
            options[23] = new Option('جاجرود', '16531');
            options[24] = new Option('چرمسازي سالاريه', '18361');
            options[25] = new Option('چهاردانگه', '33191');
            options[26] = new Option('حسن آباد', '18331');
            options[27] = new Option('حومه گلندوك', '33411');
            options[28] = new Option('خاتون آباد', '33991');
            options[29] = new Option('خاوه', '33841');
            options[30] = new Option('خرمدشت', '16571');
            options[31] = new Option('دركه', '19841');
            options[32] = new Option('دماوند', '3971');
            options[33] = new Option('رباط كريم', '3761');
            options[34] = new Option('رزگان', '37561');
            options[35] = new Option('رودهن', '39731');
            options[36] = new Option('ري', '1813');
            options[37] = new Option('سعيدآباد', '33361');
            options[38] = new Option('سلطان آباد', '37631');
            options[39] = new Option('سوهانك', '19561');
            options[40] = new Option('شاهدشهر', '33561');
            options[41] = new Option('شريف آباد', '33941');
            options[42] = new Option('شمس آباد', '18341');
            options[43] = new Option('شهر قدس', '3751');
            options[44] = new Option('شهرآباد', '33551');
            options[45] = new Option('شهرجديدپرديس', '16561');
            options[46] = new Option('شهرقدس(مويز)', '37511');
            options[47] = new Option('شهريار', '3351');
            options[48] = new Option('شهرياربردآباد', '33511');
            options[49] = new Option('صالح آباد', '33171');
            options[50] = new Option('صفادشت', '31641');
            options[51] = new Option('فرودگاه امام خميني', '18381');
            options[52] = new Option('فرون آباد', '18471');
            options[53] = new Option('فشم', '33451');
            options[54] = new Option('فيروزكوه', '3981');
            options[55] = new Option('قرچك', '18686');
            options[56] = new Option('قيام دشت', '18661');
            options[57] = new Option('كهريزك', '18161');
            options[58] = new Option('كيلان', '39751');
            options[59] = new Option('گلدسته', '33151');
            options[60] = new Option('گلستان (بهارستان)', '37571');
            options[61] = new Option('گيلاوند', '39711');
            options[62] = new Option('لواسان', '3341');
            options[63] = new Option('لوسان بزرگ', '33461');
            options[64] = new Option('مارليك', '37541');
            options[65] = new Option('مروزبهرام', '33141');
            options[66] = new Option('ملارد', '31691');
            options[67] = new Option('منطقه 11 پستي تهران', '1011');
            options[68] = new Option('منطقه 13 پستي تهران', '1013');
            options[69] = new Option('منطقه 14 پستي تهران', '1014');
            options[70] = new Option('منطقه 15 پستي تهران', '1015');
            options[71] = new Option('منطقه 16 پستي تهران', '1016');
            options[72] = new Option('منطقه 17 پستي تهران  ', '1017');
            options[73] = new Option('منطقه 18 پستي تهران  ', '1018');
            options[74] = new Option('منطقه 19 پستي تهران  ', '1019');
            options[75] = new Option('نسيم شهر (بهارستان)', '37651');
            options[76] = new Option('نصيرآباد', '37551');
            options[77] = new Option('واوان', '33176');
            options[78] = new Option('وحيديه', '33581');
            options[79] = new Option('ورامين', '3371');
            options[80] = new Option('وهن آباد', '18391');
        }
        if (state == 2) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('احمد سرگوراب', '43591');
            options[2] = new Option('اسالم', '43891');
            options[3] = new Option('اسكلك', '44681');
            options[4] = new Option('اسلام آباد', '43371');
            options[5] = new Option('اطاقور', '44791');
            options[6] = new Option('املش', '44951');
            options[7] = new Option('آبكنار', '4331');
            options[8] = new Option('آستارا', '4391');
            options[9] = new Option('آستانه اشرفيه', '4441');
            options[10] = new Option('بازاراسالم', '43731');
            options[11] = new Option('بازارجمعه شاندرمن', '43811');
            options[12] = new Option('برهسر', '44561');
            options[13] = new Option('بلترك', '44941');
            options[14] = new Option('بلسبنه', '43471');
            options[15] = new Option('بندرانزلي', '431');
            options[16] = new Option('پاشاكي', '44331');
            options[17] = new Option('پرهسر', '43861');
            options[18] = new Option('پلاسي', '43791');
            options[19] = new Option('پونل', '44992');
            options[20] = new Option('پيربست لولمان', '43441');
            options[21] = new Option('توتكابن', '44651');
            options[22] = new Option('جوكندان', '43751');
            options[23] = new Option('جيرنده', '44551');
            options[24] = new Option('چابكسر', '44871');
            options[25] = new Option('چاپارخانه', '43481');
            options[26] = new Option('چوبر', '43561');
            options[27] = new Option('خاچكين', '43451');
            options[28] = new Option('خشك بيجار', '43391');
            options[29] = new Option('خطبه سرا', '43771');
            options[30] = new Option('خمام', '4341');
            options[31] = new Option('ديلمان', '44391');
            options[32] = new Option('رانكوه', '44861');
            options[33] = new Option('رحيم آباد', '44931');
            options[34] = new Option('رستم آباد', '44641');
            options[35] = new Option('رشت', '41');
            options[36] = new Option('رضوان شهر', '43841');
            options[37] = new Option('رودبار', '4461');
            options[38] = new Option('رودسر', '4481');
            options[39] = new Option('سراوان', '43381');
            options[40] = new Option('سنگر', '43361');
            options[41] = new Option('سياهكل', '4431');
            options[42] = new Option('شاندرمن', '43851');
            options[43] = new Option('شفت', '43541');
            options[44] = new Option('صومعه سرا', '4361');
            options[45] = new Option('طاهر گوداب', '43651');
            options[46] = new Option('طوللات', '44851');
            options[47] = new Option('فومن', '4351');
            options[48] = new Option('قاسم آبادسفلي', '44831');
            options[49] = new Option('كپورچال', '43331');
            options[50] = new Option('كلاچاي', '4491');
            options[51] = new Option('كوچصفهان', '43461');
            options[52] = new Option('كومله', '44761');
            options[53] = new Option('كياشهر', '44471');
            options[54] = new Option('گشت', '43581');
            options[55] = new Option('لاهيجان', '441');
            options[56] = new Option('لشت نشا', '43431');
            options[57] = new Option('لنگرود', '4471');
            options[58] = new Option('لوشان', '44531');
            options[59] = new Option('لولمان', '43531');
            options[60] = new Option('لوندويل', '43961');
            options[61] = new Option('ليسار', '43761');
            options[62] = new Option('ماسال', '4381');
            options[63] = new Option('ماسوله', '43571');
            options[64] = new Option('منجيل', '4451');
            options[65] = new Option('هشتپر ـ طوالش', '4371');
            options[66] = new Option('واجارگاه', '44891');
        }
        if (state == 3) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('ابشاحمد', '54671');
            options[2] = new Option('اذغان', '54561');
            options[3] = new Option('اسب فروشان', '54731');
            options[4] = new Option('اسكو', '5351');
            options[5] = new Option('اغچه ريش', '5586');
            options[6] = new Option('اقمنار', '55661');
            options[7] = new Option('القو', '55541');
            options[8] = new Option('اهر', '5451');
            options[9] = new Option('ايلخچي', '53581');
            options[10] = new Option('آذرشهر', '5371');
            options[11] = new Option('باسمنج', '53661');
            options[12] = new Option('بخشايش ـ كلوانق', '53951');
            options[13] = new Option('بستان آباد', '5491');
            options[14] = new Option('بناب', '5551');
            options[15] = new Option('بناب جديد ـ مرند', '54351');
            options[16] = new Option('تبريز', '51');
            options[17] = new Option('ترك', '53331');
            options[18] = new Option('تسوج', '53881');
            options[19] = new Option('جلفا', '5441');
            options[20] = new Option('خامنه', '53841');
            options[21] = new Option('خداآفرين', '54683');
            options[22] = new Option('خسروشهر', '53551');
            options[23] = new Option('خضرلو', '55441');
            options[24] = new Option('خلجان', '53641');
            options[25] = new Option('سبلان', '5321');
            options[26] = new Option('سراب', '5471');
            options[27] = new Option('سردرود', '5361');
            options[28] = new Option('سيس', '53851');
            options[29] = new Option('شادبادمشايخ', '53671');
            options[30] = new Option('شبستر', '5381');
            options[31] = new Option('شربيان', '54751');
            options[32] = new Option('شرفخانه', '53891');
            options[33] = new Option('شهر جديد سهند', '5331');
            options[34] = new Option('صوفيان', '53861');
            options[35] = new Option('عجب شير', '5541');
            options[36] = new Option('قره اغاج ـ چاراويماق', '5581');
            options[37] = new Option('قره بابا', '54941');
            options[38] = new Option('كردكندي', '54971');
            options[39] = new Option('كليبر', '5461');
            options[40] = new Option('كندرود', '53681');
            options[41] = new Option('كندوان', '54685');
            options[42] = new Option('گوگان', '53761');
            options[43] = new Option('مراغه', '551');
            options[44] = new Option('مرند', '541');
            options[45] = new Option('ملكان', '5561');
            options[46] = new Option('ممقان', '53751');
            options[47] = new Option('ميانه', '531');
            options[48] = new Option('هاديشهر', '5431');
            options[49] = new Option('هريس', '5391');
            options[50] = new Option('هشترود', '5571');
            options[51] = new Option('هوراند', '54491');
            options[52] = new Option('ورزقان', '54581');
        }
        if (state == 4) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('اروندكنار', '6331');
            options[2] = new Option('اميديه', '63731');
            options[3] = new Option('انديمشك', '6481');
            options[4] = new Option('اهواز', '61');
            options[5] = new Option('ايذه', '6391');
            options[6] = new Option('آبادان', '631');
            options[7] = new Option('آغاجاري', '6371');
            options[8] = new Option('باغ ملك', '63951');
            options[9] = new Option('بندرامام خميني', '63561');
            options[10] = new Option('بهبهان', '6361');
            options[11] = new Option('جايزان', '63881');
            options[12] = new Option('جنت مكان', '64541');
            options[13] = new Option('چمران ـ شهرك طالقاني ', '63541');
            options[14] = new Option('حميديه', '63441');
            options[15] = new Option('خرمشهر', '641');
            options[16] = new Option('دزآب', '64651');
            options[17] = new Option('دزفول', '6461');
            options[18] = new Option('دهدز', '63991');
            options[19] = new Option('رامشير', '63871');
            options[20] = new Option('رامهرمز', '6381');
            options[21] = new Option('سربندر', '63551');
            options[22] = new Option('سردشت', '63681');
            options[23] = new Option('سماله', '64561');
            options[24] = new Option('سوسنگرد ـ دشت آزادگان', '6441');
            options[25] = new Option('شادگان', '6431');
            options[26] = new Option('شرافت', '64511');
            options[27] = new Option('شوش', '6471');
            options[28] = new Option('شوشتر', '6451');
            options[29] = new Option('شيبان', '61481');
            options[30] = new Option('صالح مشطت', '64791');
            options[31] = new Option('كردستان بزرگ', '63661');
            options[32] = new Option('گتوند', '64551');
            options[33] = new Option('لالي', '64941');
            options[34] = new Option('ماهشهر', '6351');
            options[35] = new Option('مسجد سليمان', '6491');
            options[36] = new Option('ملاثاني', '6341');
            options[37] = new Option('ميانكوه', '63751');
            options[38] = new Option('هفتگل', '64961');
            options[39] = new Option('هنديجان', '63591');
            options[40] = new Option('هويزه', '64451');
            options[41] = new Option('ويس', '61491');
        }
        if (state == 5) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option(' بيضا', '73631');
            options[2] = new Option('اردكان ـ سپيدان', '7361');
            options[3] = new Option('ارسنجان', '73761');
            options[4] = new Option('استهبان', '7451');
            options[5] = new Option('اشكنان ـ اهل', '74391');
            options[6] = new Option('اقليد', '7381');
            options[7] = new Option('اكبرآبادكوار', '71651');
            options[8] = new Option('اوز', '74331');
            options[9] = new Option('ايزدخواست', '73991');
            options[10] = new Option('آباده', '7391');
            options[11] = new Option('آباده طشك', '74931');
            options[12] = new Option('بالاده', '73391');
            options[13] = new Option('بانش', '73681');
            options[14] = new Option('بنارويه', '74361');
            options[15] = new Option('بهمن', '73911');
            options[16] = new Option('بوانات', '73941');
            options[17] = new Option('بوانات(سوريان)', '73971');
            options[18] = new Option('بيرم', '74381');
            options[19] = new Option('جنت شهر(دهخير)', '74891');
            options[20] = new Option('جهرم', '741');
            options[21] = new Option('جويم', '74351');
            options[22] = new Option('حاجي آباد ـ زرين دشت', '74861');
            options[23] = new Option('حسن آباد', '73841');
            options[24] = new Option('خرامه', '73441');
            options[25] = new Option('خرمی', '74998');
            options[26] = new Option('خشت', '73341');
            options[27] = new Option('خنج', '74431');
            options[28] = new Option('خيرآبادتوللي', '71451');
            options[29] = new Option('داراب', '7481');
            options[30] = new Option('داريان', '71461');
            options[31] = new Option('دهرم', '74781');
            options[32] = new Option('رونيز ', '74461');
            options[33] = new Option('زاهدشهر', '74671');
            options[34] = new Option('زرقان', '7341');
            options[35] = new Option('سروستان', '73451');
            options[36] = new Option('سعادت شهر ـ پاسارگاد', '73741');
            options[37] = new Option('سيدان', '73771');
            options[38] = new Option('ششده', '74651');
            options[39] = new Option('شهر جديد صدرا', '71991');
            options[40] = new Option('شيراز', '71');
            options[41] = new Option('صغاد', '73931');
            options[42] = new Option('صفاشهر ـ خرم بيد', '73951');
            options[43] = new Option('طسوج', '71641');
            options[44] = new Option('علاءمرودشت', '74441');
            options[45] = new Option('فدامي', '74871');
            options[46] = new Option('فراشبند', '74771');
            options[47] = new Option('فسا', '7461');
            options[48] = new Option('فيروزآباد', '7471');
            options[49] = new Option('فيشور', '74311');
            options[50] = new Option('قادرآباد', '73751');
            options[51] = new Option('قائميه', '7331');
            options[52] = new Option('قطب آباد', '74551');
            options[53] = new Option('قطرويه', '74981');
            options[54] = new Option('قير و كارزين', '74761');
            options[55] = new Option('كازرون', '731');
            options[56] = new Option('كام فيروز', '73431');
            options[57] = new Option('كلاني', '73141');
            options[58] = new Option('كنارتخته', '73331');
            options[59] = new Option('كوار', '73461');
            options[60] = new Option('گراش', '7441');
            options[61] = new Option('گويم', '73491');
            options[62] = new Option('لار ـ لارستان', '7431');
            options[63] = new Option('لامرد', '74341');
            options[64] = new Option('مبارك آباد', '74731');
            options[65] = new Option('مرودشت', '7371');
            options[66] = new Option('مشكان', '74971');
            options[67] = new Option('مصيري ـ رستم', '73571');
            options[68] = new Option('مظفري', '71661');
            options[69] = new Option('مهر', '74451');
            options[70] = new Option('ميمند', '74741');
            options[71] = new Option('نورآباد ـ ممسني', '7351');
            options[72] = new Option('ني ريز', '7491');
            options[73] = new Option('وراوي', '73171');
        }
        if (state == 6) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('ابريشم', '81789');
            options[2] = new Option('ابوزيدآباد', '87481');
            options[3] = new Option('اردستان', '8381');
            options[4] = new Option('اريسمان', '87641');
            options[5] = new Option('اژيه', '83781');
            options[6] = new Option('اسفرجان', '8651');
            options[7] = new Option('اسلام آباد', '86481');
            options[8] = new Option('اشن', '85451');
            options[9] = new Option('اصغرآباد', '84351');
            options[10] = new Option('اصفهان', '81');
            options[11] = new Option('امين آباد', '86531');
            options[12] = new Option('ايمان شهر', '84651');
            options[13] = new Option('آران وبيدگل', '8741');
            options[14] = new Option('بادرود', '87661');
            options[15] = new Option('باغ بهادران', '84761');
            options[16] = new Option('بهارستان', '81431');
            options[17] = new Option('بوئين ومياندشت', '85651');
            options[18] = new Option('پيربكران', '84541');
            options[19] = new Option('تودشك', '81351');
            options[20] = new Option('تيران', '8531');
            options[21] = new Option('جعفرآباد', '84381');
            options[22] = new Option('جندق', '83631');
            options[23] = new Option('جوجيل', '84691');
            options[24] = new Option('چادگان', '8571');
            options[25] = new Option('چرمهين', '84751');
            options[26] = new Option('چمگردان', '84781');
            options[27] = new Option('حسن اباد', '83791');
            options[28] = new Option('خالدآباد', '87671');
            options[29] = new Option('خميني شهر', '841');
            options[30] = new Option('خوانسار', '8791');
            options[31] = new Option('خوانسارك', '84531');
            options[32] = new Option('خور', '8361');
            options[33] = new Option('خوراسگان', '81561');
            options[34] = new Option('خورزوق', '83451');
            options[35] = new Option('داران ـ فريدن', '8561');
            options[36] = new Option('درچه پياز', '8431');
            options[37] = new Option('دستگردوبرخوار', '83431');
            options[38] = new Option('دهاقان', '8641');
            options[39] = new Option('دهق', '8541');
            options[40] = new Option('دولت آباد', '8341');
            options[41] = new Option('ديزيچه', '84831');
            options[42] = new Option('رزوه', '85761');
            options[43] = new Option('رضوان شهر', '85331');
            options[44] = new Option('رهنان', '81879');
            options[45] = new Option('زاينده رود', '84931');
            options[46] = new Option('زرين شهر ـ لنجان', '8471');
            options[47] = new Option('زواره', '8441');
            options[48] = new Option('زيار', '81681');
            options[49] = new Option('زيبا شهر', '84841');
            options[50] = new Option('سپاهان شهر', '87992');
            options[51] = new Option('سده لنجان', '84741');
            options[52] = new Option('سميرم', '8661');
            options[53] = new Option('شاهين شهر', '831');
            options[54] = new Option('شهرضا', '861');
            options[55] = new Option('شهرك صنعتي مورچ', '83331');
            options[56] = new Option('شهرك مجلسي', '8631');
            options[57] = new Option('شهرک صنعتي محمودآباد', '8161');
            options[58] = new Option('طالخونچه', '84981');
            options[59] = new Option('عسگران', '85351');
            options[60] = new Option('علويچه', '8551');
            options[61] = new Option('غرغن', '85631');
            options[62] = new Option('فرخي', '83641');
            options[63] = new Option('فريدون شهر', '8591');
            options[64] = new Option('فلاورجان', '8451');
            options[65] = new Option('فولادشهر', '8491');
            options[66] = new Option('فولادمباركه', '84881');
            options[67] = new Option('قهد ريجان', '8461');
            options[68] = new Option('كاشان', '871');
            options[69] = new Option('كليشادوسودرجان', '84561');
            options[70] = new Option('كمشچه', '83591');
            options[71] = new Option('كوهپايه', '8371');
            options[72] = new Option('گز', '83441');
            options[73] = new Option('گلپايگان', '8771');
            options[74] = new Option('گلدشت', '85831');
            options[75] = new Option('گلشهر', '87841');
            options[76] = new Option('گوگد', '8781');
            options[77] = new Option('مباركه', '8481');
            options[78] = new Option('مهاباد', '84431');
            options[79] = new Option('مورچه خورت', '8331');
            options[80] = new Option('ميمه', '8351');
            options[81] = new Option('نائين', '8391');
            options[82] = new Option('نجف آباد', '851');
            options[83] = new Option('نصر آباد', '81751');
            options[84] = new Option('نطنز', '8761');
            options[85] = new Option('نيك آباد', '83771');
            options[86] = new Option('بهارستان', '81431');
            options[87] = new Option('هرند', '83741');
            options[88] = new Option('ورزنه', '83751');
            options[89] = new Option('ورنامخواست', '84731');
            options[90] = new Option('ویلاشهر', '8581');
        }
        if (state == 7) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('ابدال آباد', '95781');
            options[2] = new Option('ازادوار', '96441');
            options[3] = new Option('باجگيران', '94861');
            options[4] = new Option('باخرز', '95971');
            options[5] = new Option('باسفر', '95481');
            options[6] = new Option('بجستان', '96981');
            options[7] = new Option('بردسكن', '9681');
            options[8] = new Option('برون', '97741');
            options[9] = new Option('بزنگان', '93871');
            options[10] = new Option('بند قرائ', '96791');
            options[11] = new Option('بيدخت', '96941');
            options[12] = new Option('تايباد', '9591');
            options[13] = new Option('تربت جام', '9571');
            options[14] = new Option('تربت حيدريه', '951');
            options[15] = new Option('جغتاي', '9641');
            options[16] = new Option('جنگل', '95471');
            options[17] = new Option('چمن آباد', '95671');
            options[18] = new Option('چناران', '9361');
            options[19] = new Option('خليل آباد', '96771');
            options[20] = new Option('خواف', '9561');
            options[21] = new Option('داورزن', '9631');
            options[22] = new Option('درگز', '9491');
            options[23] = new Option('دولت آباد ـ زاوه', '95491');
            options[24] = new Option('رادكان', '93631');
            options[25] = new Option('رشتخوار', '9541');
            options[26] = new Option('رضويه', '91671');
            options[27] = new Option('ريوش(كوهسرخ)', '96741');
            options[28] = new Option('سبزوار', '961');
            options[29] = new Option('سرخس', '9381');
            options[30] = new Option('سلطان آباد', '96561');
            options[31] = new Option('سنگان', '95641');
            options[32] = new Option('شانديز', '93561');
            options[33] = new Option('صالح آباد', '9581');
            options[34] = new Option('طرقبه ـ بينالود', '9351');
            options[35] = new Option('طوس سفلي', '93571');
            options[36] = new Option('فريمان', '9391');
            options[37] = new Option('فيروزه ـ تخت جلگه', '9331');
            options[38] = new Option('فيض آباد ـ مه ولات', '9531');
            options[39] = new Option('قاسم آباد', '95661');
            options[40] = new Option('قدمگاه', '93461');
            options[41] = new Option('قوچان', '9471');
            options[42] = new Option('كاخك', '96961');
            options[43] = new Option('كاشمر', '9671');
            options[44] = new Option('كلات', '9371');
            options[45] = new Option('گلبهار', '93651');
            options[46] = new Option('گناباد', '9691');
            options[47] = new Option('لطف آباد', '94941');
            options[48] = new Option('مشهد', '91');
            options[49] = new Option('مشهدريزه', '95961');
            options[50] = new Option('مصعبي', '97761');
            options[51] = new Option('نشتيفان', '95631');
            options[52] = new Option('نقاب ـ جوين', '96471');
            options[53] = new Option('نيشابور', '931');
            options[54] = new Option('نيل شهر', '95751');
        }
        if (state == 8) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('َآوج', '3461');
            options[2] = new Option('ارداق', '34671');
            options[3] = new Option('اسفرورين', '34561');
            options[4] = new Option('اقباليه', '34171');
            options[5] = new Option('الوند ـ البرز', '3431');
            options[6] = new Option('آبگرم', '34641');
            options[7] = new Option('آبيك', '3441');
            options[8] = new Option('آقابابا', '34791');
            options[9] = new Option('بوئين زهرا', '3451');
            options[10] = new Option('بیدستان', '34151');
            options[11] = new Option('تاكستان', '3481');
            options[12] = new Option('حصاروليعصر', '34691');
            options[13] = new Option('خاكعلي', '34481');
            options[14] = new Option('خرم دشت', '34831');
            options[15] = new Option('دانسفهان', '34581');
            options[16] = new Option('سيردان', '34741');
            options[17] = new Option('شال', '34571');
            options[18] = new Option('شهر صنعتي البرز', '3410');
            options[19] = new Option('ضياآباد', '34851');
            options[20] = new Option('قزوين', '341');
            options[21] = new Option('ليا', '34491');
            options[22] = new Option('محمديه', '3491');
            options[23] = new Option('محمود آباد نمونه', '34131');
            options[24] = new Option('معلم كلايه', '34931');
            options[25] = new Option('نرجه', '34811');
        }
        if (state == 9) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('ارادان', '35861');
            options[2] = new Option('اميريه', '3681');
            options[3] = new Option('ايوانكي', '3591');
            options[4] = new Option('بسطام', '3641');
            options[5] = new Option('بيارجمند', '3661');
            options[6] = new Option('خيرآباد', '35331');
            options[7] = new Option('دامغان', '3671');
            options[8] = new Option('درجزين', '35631');
            options[9] = new Option('سرخه', '3551');
            options[10] = new Option('سمنان', '351');
            options[11] = new Option('شاهرود', '361');
            options[12] = new Option('شهميرزاد', '3571');
            options[13] = new Option('گرمسار', '3581');
            options[14] = new Option('مجن', '3651');
            options[15] = new Option('مهدي شهر', '3561');
            options[16] = new Option('ميامي', '3631');
            options[17] = new Option('ميغان', '36441');
        }
        if (state == 10) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('دستجرد', '3741');
            options[2] = new Option('سلفچگان', '37461');
            options[3] = new Option('شهر جعفریه', '37441');
            options[4] = new Option('قم', '371');
            options[5] = new Option('قنوات', '3731');
            options[6] = new Option('كهك', '37351');
        }
        if (state == 11) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('اراك', '381');
            options[2] = new Option('آستانه', '3871');
            options[3] = new Option('آشتيان', '3961');
            options[4] = new Option('تفرش', '3951');
            options[5] = new Option('توره', '38661');
            options[6] = new Option('جاورسيان', '38451');
            options[7] = new Option('خسروبيك', '38541');
            options[8] = new Option('خشك رود', '37761');
            options[9] = new Option('خمين', '3881');
            options[10] = new Option('خنداب', '3841');
            options[11] = new Option('دليجان', '3791');
            options[12] = new Option('ريحان عليا', '38941');
            options[13] = new Option('زاويه', '39441');
            options[14] = new Option('ساوه', '391');
            options[15] = new Option('شازند', '3861');
            options[16] = new Option('شهراب', '39541');
            options[17] = new Option('شهرك مهاجران', '3991');
            options[18] = new Option('فرمهين', '39531');
            options[19] = new Option('كميجان', '3851');
            options[20] = new Option('مامونيه ـ زرنديه', '3941');
            options[21] = new Option('محلات', '3781');
            options[22] = new Option('ميلاجرد', '38551');
            options[23] = new Option('هندودر', '38761');
        }
        if (state == 12) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option(' آب بر ـ طارم', '4591');
            options[2] = new Option('ابهر', '4561');
            options[3] = new Option('اسفجين', '45371');
            options[4] = new Option('پري', '45431');
            options[5] = new Option('حلب', '45971');
            options[6] = new Option('خرمدره', '4571');
            options[7] = new Option('دستجرده', '45941');
            options[8] = new Option('دندي', '45471');
            options[9] = new Option('زرين آباد ـ ايجرود', '4531');
            options[10] = new Option('زرين رود', '45881');
            options[11] = new Option('زنجان', '451');
            options[12] = new Option('سلطانيه', '4551');
            options[13] = new Option('صائين قلعه', '45741');
            options[14] = new Option('قيدار', '4581');
            options[15] = new Option('گرماب', '45871');
            options[16] = new Option('گيلوان', '45931');
            options[17] = new Option('ماهنشان', '4541');
            options[18] = new Option('همايون', '45331');
            options[19] = new Option('هيدج', '45731');
        }
        if (state == 13) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('اسلام آباد', '48451');
            options[2] = new Option('اميركلا', '4731');
            options[3] = new Option('ايزدشهر', '46411');
            options[4] = new Option('آمل', '461');
            options[5] = new Option('آهنگركلا', '47341');
            options[6] = new Option('بابل', '471');
            options[7] = new Option('بابلسر', '4741');
            options[8] = new Option('بلده', '46471');
            options[9] = new Option('بهشهر', '4851');
            options[10] = new Option('بهنمير', '47441');
            options[11] = new Option('پل سفيد ـ سوادكوه', '4791');
            options[12] = new Option('تنكابن', '4681');
            options[13] = new Option('جويبار', '4771');
            options[14] = new Option('چالوس', '4661');
            options[15] = new Option('چمستان', '46431');
            options[16] = new Option('خرم آباد', '46851');
            options[17] = new Option('خوشرودپی', '47331');
            options[18] = new Option('رامسر', '4691');
            options[19] = new Option('رستم كلا', '48561');
            options[20] = new Option('رويانشهر', '46561');
            options[21] = new Option('زاغمرز', '48541');
            options[22] = new Option('زرگر محله', '47581');
            options[23] = new Option('زيرآب', '4781');
            options[24] = new Option('سادات محله', '46931');
            options[25] = new Option('ساري', '481');
            options[26] = new Option('سرخرود', '46341');
            options[27] = new Option('سلمانشهر', '4671');
            options[28] = new Option('سنگده', '48351');
            options[29] = new Option('سوا', '46371');
            options[30] = new Option('سورك', '48441');
            options[31] = new Option('شيرگاه', '47871');
            options[32] = new Option('شيرود', '46861');
            options[33] = new Option('عباس آباد', '46741');
            options[34] = new Option('فريدون كنار', '4751');
            options[35] = new Option('قائم شهر', '4761');
            options[36] = new Option('كلارآباد', '46731');
            options[37] = new Option('كلاردشت', '46661');
            options[38] = new Option('كيا كلا', '47731');
            options[39] = new Option('كياسر', '4831');
            options[40] = new Option('گزنك', '46391');
            options[41] = new Option('گلوگاه', '4861');
            options[42] = new Option('گهرباران', '48461');
            options[43] = new Option('محمودآباد', '4631');
            options[44] = new Option('مرزن آباد', '46641');
            options[45] = new Option('مرزي كلا', '47561');
            options[46] = new Option('نشتارود', '46831');
            options[47] = new Option('نكاء', '4841');
            options[48] = new Option('نور', '4641');
            options[49] = new Option('نوشهر', '4651');
        }
        if (state == 14) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('انبار آلوم', '49391');
            options[2] = new Option('اينچه برون', '49751');
            options[3] = new Option('آزادشهر', '4961');
            options[4] = new Option('آق قلا', '4931');
            options[5] = new Option('بندر گز', '4871');
            options[6] = new Option('بندرتركمن', '4891');
            options[7] = new Option('جلين', '49351');
            options[8] = new Option('خان ببين', '49531');
            options[9] = new Option('راميان', '4951');
            options[10] = new Option('سيمين شهر', '48971');
            options[11] = new Option('علي آباد', '4941');
            options[12] = new Option('فاضل آباد', '49431');
            options[13] = new Option('كردكوي', '4881');
            options[14] = new Option('كلاله', '4991');
            options[15] = new Option('گاليكش', '49831');
            options[16] = new Option('گرگان', '491');
            options[17] = new Option('گميش تپه', '48961');
            options[18] = new Option('گنبدكاوس', '4971');
            options[19] = new Option('مراوه تپه', '48733');
            options[20] = new Option('مينودشت', '4981');
        }
        if (state == 15) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('ابي بيگلو', '56331');
            options[2] = new Option('اردبيل', '561');
            options[3] = new Option('اصلاندوز', '56981');
            options[4] = new Option('بيله سوار', '5671');
            options[5] = new Option('پارس آباد', '5691');
            options[6] = new Option('تازه كند انگوت', '56581');
            options[7] = new Option('جعفرآباد', '56751');
            options[8] = new Option('خلخال', '5681');
            options[9] = new Option('سرعين', '56391');
            options[10] = new Option('شهرك شهيد غفاري', '56971');
            options[11] = new Option('كلور', '56891');
            options[12] = new Option('كوارئيم', '56431');
            options[13] = new Option('گرمي ', '5651');
            options[14] = new Option('گيوي ـ كوثر', '56851');
            options[15] = new Option('لاهرود', '56653');
            options[16] = new Option('مشگين شهر', '5661');
            options[17] = new Option('نمين', '5631');
            options[18] = new Option('نير', '5641');
            options[19] = new Option('هشتجين', '56871');
        }
        if (state == 16) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('اروميه', '571');
            options[2] = new Option('اشنويه', '5771');
            options[3] = new Option('ايواوغلي', '5831');
            options[4] = new Option('بازرگان', '58671');
            options[5] = new Option('بوكان', '5951');
            options[6] = new Option('پسوه', '57951');
            options[7] = new Option('پلدشت', '58771');
            options[8] = new Option('پيرانشهر', '5781');
            options[9] = new Option('تازه شهر', '5891');
            options[10] = new Option('تكاب', '5991');
            options[11] = new Option('چهاربرج قديم', '59771');
            options[12] = new Option('خوي', '581');
            options[13] = new Option('ديزج', '57451');
            options[14] = new Option('ديزجديز', '5837');
            options[15] = new Option('ربط', '59691');
            options[16] = new Option('زيوه', '57461');
            options[17] = new Option('سردشت', '5961');
            options[18] = new Option('سلماس', '5881');
            options[19] = new Option('سيلوانا', '57411');
            options[20] = new Option('سيلوه', '573');
            options[21] = new Option('سيه چشمه ـ چالدران', '5871');
            options[22] = new Option('شاهين دژ', '5981');
            options[23] = new Option('شوط', '58751');
            options[24] = new Option('قره ضياء الدين ـ چايپاره', '5851');
            options[25] = new Option('قوشچي', '5751');
            options[26] = new Option('كشاورز (اقبال)', '59731');
            options[27] = new Option('ماكو', '5861');
            options[28] = new Option('محمد يار', '57661');
            options[29] = new Option('محمودآباد', '59861');
            options[30] = new Option('مهاباد', '591');
            options[31] = new Option('مياندوآب', '5971');
            options[32] = new Option('مياوق', '57351');
            options[33] = new Option('ميرآباد', '59671');
            options[34] = new Option('نقده', '5761');
            options[35] = new Option('نوشين شهر', '57381');
        }
        if (state == 17) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('ازندريان', '65995');
            options[2] = new Option('اسدآباد', '6541');
            options[3] = new Option('اسلام آباد', '65791');
            options[4] = new Option('بهار', '6531');
            options[5] = new Option('پايگاه نوژه', '65992');
            options[6] = new Option('تويسركان', '6581');
            options[7] = new Option('دمق', '65671');
            options[8] = new Option('رزن', '65681');
            options[9] = new Option('سامن', '65761');
            options[10] = new Option('سركان', '65841');
            options[11] = new Option('شيرين سو', '65571');
            options[12] = new Option('صالح آباد', '65361');
            options[13] = new Option('فامنين', '6561');
            options[14] = new Option('قروه درجزين', '65691');
            options[15] = new Option('قهاوند', '65631');
            options[16] = new Option('كبودرآهنگ', '6551');
            options[17] = new Option('گيان', '65961');
            options[18] = new Option('لالجين', '65331');
            options[19] = new Option('ملاير', '6571');
            options[20] = new Option('نهاوند', '6591');
            options[21] = new Option('همدان', '651');
        }
        if (state == 18) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('اورامانتخت', '66791');
            options[2] = new Option('بانه', '6691');
            options[3] = new Option('بلبان آباد', '66661');
            options[4] = new Option('بيجار', '6651');
            options[5] = new Option('دلبران', '66631');
            options[6] = new Option('دهگلان', '66671');
            options[7] = new Option('ديواندره', '6641');
            options[8] = new Option('سروآباد', '66781');
            options[9] = new Option('سريش آباد', '66691');
            options[10] = new Option('سقز', '6681');
            options[11] = new Option('سنندج', '661');
            options[12] = new Option('قروه', '6661');
            options[13] = new Option('كامياران', '6631');
            options[14] = new Option('مريوان', '6671');
            options[15] = new Option('موچش', '66391');
        }
        if (state == 19) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('اسلام آباد غرب', '6761');
            options[2] = new Option('باينگان', '67931');
            options[3] = new Option('بيستون', '67371');
            options[4] = new Option('پاوه', '6791');
            options[5] = new Option('تازه آباد ـ ثلاث باباجاني', '67771');
            options[6] = new Option('جوانرود', '67981');
            options[7] = new Option('روانسر', '67961');
            options[8] = new Option('ريجاب', '67651');
            options[9] = new Option('سراب ذهاب', '67741');
            options[10] = new Option('سرپل ذهاب', '6771');
            options[11] = new Option('سنقر', '6751');
            options[12] = new Option('صحنه', '67461');
            options[13] = new Option('فرامان', '67441');
            options[14] = new Option('فش', '67431');
            options[15] = new Option('قصرشيرين', '6781');
            options[16] = new Option('كرمانشاه', '671');
            options[17] = new Option('كنگاور', '6741');
            options[18] = new Option('گيلانغرب', '67871');
            options[19] = new Option('نودشه', '67951');
            options[20] = new Option('هرسين', '6731');
            options[21] = new Option('هلشي', '67341');
        }
        if (state == 20) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('ازنا', '6871');
            options[2] = new Option('الشتر ـ سلسله', '6891');
            options[3] = new Option('اليگودرز', '6861');
            options[4] = new Option('برخوردار', '68331');
            options[5] = new Option('بروجرد', '691');
            options[6] = new Option('پل دختر', '6851');
            options[7] = new Option('تقي آباد', '68391');
            options[8] = new Option('چغلوندی', '68181');
            options[9] = new Option('چقابل', '68451');
            options[10] = new Option('خرم آباد', '681');
            options[11] = new Option('دورود', '6881');
            options[12] = new Option('زاغه', '68761');
            options[13] = new Option('سپيددشت', '68861');
            options[14] = new Option('شول آباد', '68671');
            options[15] = new Option('كوناني', '68471');
            options[16] = new Option('كوهدشت', '6841');
            options[17] = new Option('معمولان', '68571');
            options[18] = new Option('نورآباد ـ دلفان', '6831');
            options[19] = new Option('واشيان نصيرتپه', '68541');
        }
        if (state == 21) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('ابدان', '75551');
            options[2] = new Option('اهرم ـ تنگستان', '7551');
            options[3] = new Option('آباد', '75491');
            options[4] = new Option('آبپخش', '75651');
            options[5] = new Option('بادوله', '75431');
            options[6] = new Option('برازجان ـ دشتستان', '7561');
            options[7] = new Option('بردخون', '75531');
            options[8] = new Option('بندردير', '75541');
            options[9] = new Option('بندرديلم', '75361');
            options[10] = new Option('بندرريگ', '75331');
            options[11] = new Option('بندركنگان', '75571');
            options[12] = new Option('بندرگناوه', '7531');
            options[13] = new Option('بوشهر', '751');
            options[14] = new Option('تنگ ارم', '75681');
            options[15] = new Option('جزيره خارك', '75461');
            options[16] = new Option('جم', '75581');
            options[17] = new Option('چغارك', '75381');
            options[18] = new Option('خورموج ـ دشتي', '7541');
            options[19] = new Option('دلوار', '75471');
            options[20] = new Option('ريز', '75561');
            options[21] = new Option('سعدآباد', '75661');
            options[22] = new Option('شبانكاره', '75641');
            options[23] = new Option('شنبه', '75441');
            options[24] = new Option('شول', '75351');
            options[25] = new Option('عالی شهر', '75196');
            options[26] = new Option('عسلويه', '75391');
            options[27] = new Option('كاكي', '75451');
            options[28] = new Option('كلمه', '75691');
            options[29] = new Option('نخل تقي', '75111');
            options[30] = new Option('وحدتيه', '75671');
        }
        if (state == 22) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('اختيارآباد', '76381');
            options[2] = new Option('ارزوئیه', '78591');
            options[3] = new Option('امين شهر', '77431');
            options[4] = new Option('انار', '7741');
            options[5] = new Option('باغين', '76371');
            options[6] = new Option('بافت', '7851');
            options[7] = new Option('بردسير', '7841');
            options[8] = new Option('بلوك', '78791');
            options[9] = new Option('بم', '7661');
            options[10] = new Option('بهرمان', '77461');
            options[11] = new Option('پاريز', '7831');
            options[12] = new Option('جواديه فلاح', '77471');
            options[13] = new Option('جوشان', '76431');
            options[14] = new Option('جيرفت', '7861');
            options[15] = new Option('چترود', '7791');
            options[16] = new Option('خانوك', '77761');
            options[17] = new Option('دوساري', '78771');
            options[18] = new Option('رابر', '78561');
            options[19] = new Option('راور', '7651');
            options[20] = new Option('راين', '7681');
            options[21] = new Option('رفسنجان', '771');
            options[22] = new Option('رودبار', '78831');
            options[23] = new Option('ريگان', '76761');
            options[24] = new Option('زرند', '7761');
            options[25] = new Option('زنگي آباد', '76391');
            options[26] = new Option('سرچشمه', '7731');
            options[27] = new Option('سريز', '77751');
            options[28] = new Option('سيرجان', '781');
            options[29] = new Option('شهربابك', '7751');
            options[30] = new Option('صفائيه', '77391');
            options[31] = new Option('عنبرآباد', '7871');
            options[32] = new Option('فارياب', '78871');
            options[33] = new Option('فهرج', '76741');
            options[34] = new Option('قلعه گنج', '78841');
            options[35] = new Option('كاظم آباد', '77951');
            options[36] = new Option('كرمان', '761');
            options[37] = new Option('كهنوج', '7881');
            options[38] = new Option('كهنوج( مغزآباد)', '77941');
            options[39] = new Option('كوهبنان', '7781');
            options[40] = new Option('كيان شهر', '7771');
            options[41] = new Option('گلباف', '7641');
            options[42] = new Option('ماهان', '7631');
            options[43] = new Option('محمدآباد ـ ريگان', '7691');
            options[44] = new Option('محي آباد', '76891');
            options[45] = new Option('منوجان', '7891');
            options[46] = new Option('نجف شهر', '78151');
            options[47] = new Option('نگار', '78431');
        }
        if (state == 23) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('ابوموسي', '79591');
            options[2] = new Option('ايسين', '79331');
            options[3] = new Option('بستك', '7961');
            options[4] = new Option('بندرخمير', '7931');
            options[5] = new Option('بندرعباس', '791');
            options[6] = new Option('بندرلنگه', '7971');
            options[7] = new Option('بندزك كهنه', '79981');
            options[8] = new Option('پارسيان', '79771');
            options[9] = new Option('پدل', '79631');
            options[10] = new Option('پل شرقي', '79341');
            options[11] = new Option('تياب', '79971');
            options[12] = new Option('جاسك', '79791');
            options[13] = new Option('جزيره سيري', '79581');
            options[14] = new Option('جزيره لاوان', '79781');
            options[15] = new Option('جزيره هنگام', '79571');
            options[16] = new Option('جزيرهلارك', '79561');
            options[17] = new Option('جناح', '79611');
            options[18] = new Option('چارك', '79751');
            options[19] = new Option('حاجي آباد', '79391');
            options[20] = new Option('درگهان', '79531');
            options[21] = new Option('دشتي', '79761');
            options[22] = new Option('دهبارز ـ رودان', '7991');
            options[23] = new Option('رويدر', '79661');
            options[24] = new Option('زيارت علي', '79941');
            options[25] = new Option('سردشت ـ بشاگرد', '79881');
            options[26] = new Option('سندرك', '79841');
            options[27] = new Option('سيريك', '79461');
            options[28] = new Option('فارغان', '79371');
            options[29] = new Option('فين', '79351');
            options[30] = new Option('قشم', '7951');
            options[31] = new Option('كنگ', '79641');
            options[32] = new Option('كيش', '7941');
            options[33] = new Option('ميناب', '7981');
        }
        if (state == 24) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('اردل', '8881');
            options[2] = new Option('آلوني', '88941');
            options[3] = new Option('باباحيدر', '88631');
            options[4] = new Option('بروجن', '8871');
            options[5] = new Option('بلداجي', '88761');
            options[6] = new Option('بن', '88581');
            options[7] = new Option('جونقان', '88671');
            options[8] = new Option('چالشتر', '88471');
            options[9] = new Option('چلگرد ـ كوهرنگ', '88651');
            options[10] = new Option('دزك', '8834');
            options[11] = new Option('دستنائ', '88361');
            options[12] = new Option('دشتك', '88881');
            options[13] = new Option('سامان', '8851');
            options[14] = new Option('سودجان', '88461');
            options[15] = new Option('سورشجان', '88431');
            options[16] = new Option('شلمزار ـ كيار', '88371');
            options[17] = new Option('شهركرد', '881');
            options[18] = new Option('فارسان', '8861');
            options[19] = new Option('فرادنبه', '88741');
            options[20] = new Option('فرخ شهر', '8831');
            options[21] = new Option('كیان', '88139');
            options[22] = new Option('گندمان', '88781');
            options[23] = new Option('گهرو', '88381');
            options[24] = new Option('لردگان', '8891');
            options[25] = new Option('مال خليفه', '88951');
            options[26] = new Option('ناغان', '88831');
            options[27] = new Option('هاروني', '8844');
            options[28] = new Option('هفشجان', '8841');
            options[29] = new Option('وردنجان', '88571');
        }
        if (state == 25) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('ابركوه', '8931');
            options[2] = new Option('احمدآباد', '89531');
            options[3] = new Option('اردكان', '8951');
            options[4] = new Option('بافق', '8971');
            options[5] = new Option('بفروئيه', '89631');
            options[6] = new Option('بهاباد', '89761');
            options[7] = new Option('تفت', '8991');
            options[8] = new Option('حميديا', '89491');
            options[9] = new Option('زارچ', '89418');
            options[10] = new Option('شاهديه', '89431');
            options[11] = new Option('صدوق', '8941');
            options[12] = new Option('طبس', '9791');
            options[13] = new Option('عشق آباد', '97981');
            options[14] = new Option('فراغه', '89331');
            options[15] = new Option('مروست', '89871');
            options[16] = new Option('مهريز', '8981');
            options[17] = new Option('ميبد', '8961');
            options[18] = new Option('نير', '89961');
            options[19] = new Option('هرات ـ خاتم', '89881');
            options[20] = new Option('يزد', '891');
        }
        if (state == 26) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('اسپكه', '99431');
            options[2] = new Option('ايرانشهر', '991');
            options[3] = new Option('بزمان', '99491');
            options[4] = new Option('بمپور', '9941');
            options[5] = new Option('بنت', '99451');
            options[6] = new Option('بنجار', '98691');
            options[7] = new Option('پسكو', '99641');
            options[8] = new Option('تيموراباد', '98641');
            options[9] = new Option('جالق', '99561');
            options[10] = new Option('چابهار', '9971');
            options[11] = new Option('خاش', '9891');
            options[12] = new Option('دوست محمد ـ هيرمند', '9851');
            options[13] = new Option('راسك', '99361');
            options[14] = new Option('زابل', '9861');
            options[15] = new Option('زابلي', '99661');
            options[16] = new Option('زاهدان', '981');
            options[17] = new Option('زهك', '9871');
            options[18] = new Option('ساربوك', '99991');
            options[19] = new Option('سراوان', '9951');
            options[20] = new Option('سرباز', '9931');
            options[21] = new Option('سنگان', '98971');
            options[22] = new Option('سوران ـ سيب سوران', '9961');
            options[23] = new Option('سيركان', '99571');
            options[24] = new Option('فنوج', '99461');
            options[25] = new Option('قصرقند', '99961');
            options[26] = new Option('كنارك', '9981');
            options[27] = new Option('كيتج', '99881');
            options[28] = new Option('گلمورتي ـ دلگان', '99471');
            options[29] = new Option('گوهركوه', '98931');
            options[30] = new Option('محمدآباد', '98681');
            options[31] = new Option('ميرجاوه', '9841');
            options[32] = new Option('نصرت آباد', '9831');
            options[33] = new Option('نگور', '99761');
            options[34] = new Option('نيك شهر', '9991');
            options[35] = new Option('هيدوچ', '99671');
        }
        if (state == 27) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('اركواز', '69971');
            options[2] = new Option('ارمو', '69641');
            options[3] = new Option('ايلام', '6931');
            options[4] = new Option('ايوان', '6941');
            options[5] = new Option('آبدانان', '6971');
            options[6] = new Option('آسمان آباد', '69561');
            options[7] = new Option('بدره', '69671');
            options[8] = new Option('توحيد', '69531');
            options[9] = new Option('چشمه شيرين', '69661');
            options[10] = new Option('چوار', '69361');
            options[11] = new Option('دره شهر', '6961');
            options[12] = new Option('دهلران', '6981');
            options[13] = new Option('سرابله ـ شيروان و چرداول', '6951');
            options[14] = new Option('شباب ', '69511');
            options[15] = new Option('شهرك اسلاميه', '69931');
            options[16] = new Option('لومار', '69551');
            options[17] = new Option('مهران', '6991');
            options[18] = new Option('موسيان', '69841');
            options[19] = new Option('ميمه', '69861');
        }
        if (state == 28) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('باشت', '75881');
            options[2] = new Option('پاتاوه', '75981');
            options[3] = new Option('چرام', '75761');
            options[4] = new Option('دهدشت ـ كهگيلويه', '7571');
            options[5] = new Option('دوگنبدان ـ گچساران', '7581');
            options[6] = new Option('ديشموك', '75771');
            options[7] = new Option('سپيدار', '75931');
            options[8] = new Option('سوق', '75731');
            options[9] = new Option('سي سخت ـ دنا', '75991');
            options[10] = new Option('قلعه رئيسي', '75781');
            options[11] = new Option('لنده', '75741');
            options[12] = new Option('ليكك', '75751');
            options[13] = new Option('مادوان', '75911');
            options[14] = new Option('ياسوج ـ 7591', '7591');
        }
        if (state == 29) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('اسفراين', '9661');
            options[2] = new Option('ايور', '94331');
            options[3] = new Option('آشخانه ـ مانه و سلمقان', '9451');
            options[4] = new Option('بجنورد', '941');
            options[5] = new Option('جاجرم', '9441');
            options[6] = new Option('درق', '94311');
            options[7] = new Option('راز', '94561');
            options[8] = new Option('شوقان', '94471');
            options[9] = new Option('شيروان', '9461');
            options[10] = new Option('فاروج', '9481');
            options[11] = new Option('گرمه', '9431');
        }
        if (state == 30) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('ارسك', '97831');
            options[2] = new Option('اسديه ـ درميان', '97441');
            options[3] = new Option('آرين شهر', '97631');
            options[4] = new Option('آيسك', '97791');
            options[5] = new Option('بشرويه', '9781');
            options[6] = new Option('بیرجند', '971');
            options[7] = new Option('حاجي آباد', '97671');
            options[8] = new Option('خضري دشت بياض', '97661');
            options[9] = new Option('خوسف', '97351');
            options[10] = new Option('زهان', '97691');
            options[11] = new Option('سر بیشه', '9741');
            options[12] = new Option('سرايان', '97771');
            options[13] = new Option('سه قلعه', '97891');
            options[14] = new Option('فردوس', '9771');
            options[15] = new Option('قائن ـ قائنات', '9761');
            options[16] = new Option('گزيک', '97461');
            options[17] = new Option('مود', '97311');
            options[18] = new Option('نهبندان', '9751');
            options[19] = new Option('نیمبلوك', '97443');
        }
        if (state == 31) {
            options[0] = new Option('لطفا شهر را انتخاب نمایید', '0');
            options[1] = new Option('اشتهارد', '31871');
            options[2] = new Option('آسارا', '31551');
            options[3] = new Option('چهارباغ', '33661');
            options[4] = new Option('سيف آباد', '33611');
            options[5] = new Option('شهر جديد هشتگرد', '33618');
            options[6] = new Option('طالقان', '33691');
            options[7] = new Option('كرج', '31');
            options[8] = new Option('كمال شهر', '31991');
            options[9] = new Option('كوهسار ـ چندار', '33651');
            options[10] = new Option('گرمدره', '31638');
            options[11] = new Option('ماهدشت', '31849');
            options[12] = new Option('محمدشهر', '31778');
            options[13] = new Option('مشکين دشت', '31776');
            options[14] = new Option('نظرآباد', '3331');
            options[15] = new Option('هشتگرد ـ ساوجبلاغ', '3361');
        }
    }
}

//این تابع برای نمایش آدرس کامل در بخش نمایش آدرس است
function showAddress() {
    var state = document.getElementById("state").options[document.getElementById("state").selectedIndex].text;
    var city = document.getElementById("city").options[document.getElementById("city").selectedIndex].text;
    var address = document.getElementById("address").value;
    var postal_code = document.getElementById("postal_code").value;
    var mobile = document.getElementById("mobile").value;
    var full_address = state + " - " + city + " - " + address + " - " + postal_code + " - " + mobile;
    document.getElementById("full_address").innerHTML = full_address;
}

function replyComment(parentId, url, csrfToken) {
    let commentElementId = "comment-" + parentId;
    let replyButtonId = "reply-btn-" + parentId;
    console.log(commentElementId)
    let commentElement = document.getElementById(commentElementId);
    let replyForm = document.createElement("form");
    let csrfTokenInput = document.createElement("input")
    let replyParentInput = document.createElement("input");
    let replyTextArea = document.createElement("textarea");
    let replySendButton = document.createElement("button");

    replyForm.className = "global-form";
    replyForm.method = "post";
    replyForm.action = url;

    csrfTokenInput.name = "csrfmiddlewaretoken";
    csrfTokenInput.type = "hidden";
    console.log(csrfToken);
    csrfTokenInput.value = csrfToken;

    replyParentInput.value = parentId;
    replyParentInput.name = "parent";
    replyParentInput.type = "hidden";

    replyTextArea.type = "text";
    replyTextArea.name = "content";
    replyTextArea.textarea = "پاسخ خود را بنویسید";
    replyTextArea.placeholder = "پاسخ خود را بنویسید";

    replySendButton.type = "submit";
    replySendButton.innerText = "ارسال";
    // replySendButton.addEventListener("click", function () {
    //     showReplySentMessage(commentElement);
    //     replyForm.remove();
    //     return true;
    // });

    replyForm.appendChild(csrfTokenInput);
    replyForm.appendChild(replyParentInput);
    replyForm.appendChild(replyTextArea);
    replyForm.appendChild(replySendButton);
    commentElement.appendChild(replyForm);
    document.getElementById(replyButtonId).remove();
}

function showReplySentMessage(commentElement) {
    var messageElement = document.createElement("div");
    messageElement.className = "message";
    messageElement.className = "alert alert-success";
    messageElement.innerText = " نظر شما ثبت شد و پس از تایید نمایش داده خواهد شد";
    commentElement.appendChild(messageElement);
}

