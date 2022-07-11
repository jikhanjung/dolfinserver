var BIRDNAME_LIST=[
	["가창오리", "Anas formosa"],
	["개리", "Anser cygnoides"],
	["고니", "Cygnus columbianus"],
	["고방오리", "Anas acuta"],
	["넓적부리", "Anas clypeata"],
	["죽지", "Aythya fuligula"],
	["미국쇠오리", "Anas crecca carolinensis"],
	["바다꿩", "Clangula hyemalis"],
	["비오리", "Mergus serrator"],
	["발구지", "Anas querquedula"],
	["비오리", "Mergus merganser"],
	["쇠기러기", "Anser albifrons"],
	["쇠오리", "Anas crecca crecca"],
	["아메리카홍머리오리", "Anas americana"],
	["알락오리", "Anas strepera"],
	["원앙", "Aix galericulata"],
	["원앙사촌", "Tadorna cristata (1916년 최후 기록이)"],
	["청둥오리", "Anas platyrhynchos"],
	["청머리오리", "Anas falcata"],
	["큰고니", "Cygnus cygnus"],
	["큰기러기", "Anser fabalis"],
	["호사비오리", "Mergus squamatus"],
	["혹고니", "Cygnus olor"],
	["혹부리오리", "Tadorna tadorna"],
	["홍머리오리", "Anas penelope"],
	["미국오리", "Anas rubripes"],
	["검은목논병아리", "Podiceps nigricollis"],
	["귀뿔논병아리", "Podiceps auritus"],
	["논병아리", "Tachybaptus ruficollis"],
	["뿔논병아리", "Podiceps cristatus"],
	["큰논병아리", "Podiceps grisegena"],
	["꿩", "Phasianus colchicus"],
	["들꿩", "Bonasa bonasia"],
	["메추라기", "Coturnix japonica"],
	["닭", "Tetrao tetrix"],
	["갈매기", "Larus canus"],
	["괭이갈매기", "Larus crassirostris"],
	["세가락갈매기", "Rissa tridactyla"],
	["쇠목테갈매기", "Rhodostethia rosea"],
	["쇠제비갈매기", "Sterna albifrons"],
	["수리갈매기", "Larus glaucescens"],
	["카스피해갈매기", "Larus cachinnans"],
	["큰재갈매기", "Larus schistisagus"],
	["북극도둑갈매기", "Stercorarius parasiticus"],
	["긴부리도요", "Limnodromus scolopaceus"],
	["깝작도요", "Actitis hypoleucos (Tringa?)"],
	["꺅도요", "Gallinago gallinago"],
	["꺅도요사촌", "Gallinago megala"],
	["꼬까도요", "Arenaria interpres"],
	["꼬마도요", "Lymnocryptes minimus (1916년 최후 기록이)"],
	["넓적부리도요", "Eurynorhynchus pygmeus"],
	["뒷부리도요", "Xenus cinereus (Tringa cinerea?)"],
	["마도요", "Numenius arquata"],
	["메추라기도요", "Calidris acuminata"],
	["멧도요", "Scolopax rusticola"],
	["목도리도요", "Philomachus pugnax"],
	["민물도요", "Calidris alpina"],
	["바늘꼬리도요", "Gallinago stenura"],
	["삑삑도요", "Tringa ochropus"],
	["세가락도요", "Calidris alba"],
	["송곳부리도요", "Limicola falcinellus"],
	["쇠부리도요", "Numenius minutus"],
	["쇠청다리도요", "Tringa stagnatilis"],
	["아메리카메추라기도요", "Calidris melanotos"],
	["알락꼬리마도요", "Numenius madagascariensis"],
	["알락도요", "Tringa glareola"],
	["작은도요", "Calidris minuta"],
	["좀도요", "Calidris ruficollis"],
	["종달도요", "Calidris subminuta"],
	["중부리도요", "Numenius phaeopus"],
	["지느러미발도요", "Phalaropus lobatus"],
	["큰꺅도요", "Gallinago hardwickii"],
	["큰뒷부리도요", "Limosa lapponica"],
	["큰부리도요", "Limnodromus semipalmatus"],
	["큰지느러미발도요", "Phalaropus tricolor"],
	["학도요", "Tringa erythropus"],
	["물꿩", "Hydrophasianus chirurgus"],
	["개꿩", "Pluvialis squatarola"],
	["꼬마물떼새", "Charadrius dubius"],
	["댕기물떼새", "Vanellus vanellus"],
	["뒷부리장다리물떼새", "Recurvirostra avosetta"],
	["민댕기물떼새", "Vanellus cinereus"],
	["왕눈물떼새", "Charadrius mongolus"],
	["장다리물떼새", "Himantopus himantopus"],
	["큰왕눈물떼새", "Charadrius leschenaultii"],
	["바다오리", "Uria aalge"],
	["바다쇠오리", "Synthliboramphus antiquus"],
	["뿔쇠오리", "Synthliboramphus wumizusume"],
	["알랑쇠오리", "Brachyramphus marmoratus"],
	["작은바다오리", "Aethia pusilla"],
	["구레나룻제비갈매기", "Chlidonias hybridus"],
	["제비갈매기", "Sterna hirundo"],
	["큰부리제비갈매기", "Sterna nilotica"],
	["큰제비갈매기", "Sterna bergii"],
	["제비물떼새", "Glareola maldivarum"],
	["호사도요", "Rostratula benghalensis"],
	["느시", "Otis tarda"],
	["검은목두루미", "Grus grus"],
	["두루미", "Grus japonensis"],
	["캐나다두루미", "Grus canadensis"],
	["뜸부기", "Gallicrex cinerea"],
	["물닭", "Fulica atra"],
	["쇠뜸부기", "Porzana pusilla"],
	["쇠뜸부기사촌", "Porzana fusca"],
	["쇠물닭", "Gallinula chloropus"],
	["알락뜸부기", "Coturnicops exquisitus"],
	["한국뜸부기", "Porzana paykullii"],
	["개미잡이", "Jynx torquilla"],
	["세가락딱따구리", "Picoides tridactylus"],
	["쇠딱따구리", "Dendrocopos kizuki"],
	["아무르쇠딱따구리", "Dendrocopos canicapillus"],
	["크낙새", "Dryocopus javensis"],
	["매", "Falco peregrinus"],
	["비둘기조롱이", "Falco vespertinus"],
	["새홀리기", "Falco subbuteo"],
	["쇠황조롱이", "Falco columbarius"],
	["헨다손매", "Falco cherrug"],
	["황조롱이", "Falco tinnunculus"],
	["녹색비둘기", "Treron sieboldii"],
	["멧비둘기", "Streptopelia orientalis"],
	["염주비둘기", "Streptopelia decaocto"],
	["양비둘기", "Columba rupestris"],
	["두견이", "Cuculus poliocephalus"],
	["매사촌", "Cuculus fugax"],
	["벙어리뻐꾸기", "Cuculus saturatus"],
	["뻐꾸기", "Cuculus canorus"],
	["가마우지", "Phalacrocorax capillatus"],
	["민물가마우지", "Phalacrocorax carbo"],
	["쇠가마우지", "Phalacrocorax pelagicus"],
	["군함조", "Fregata ariel"],
	["큰군함조", "Fregata minor"],
	["사다새", "Pelecanus philippensis"],
	["세가락메추라기", "Turnix tanki"],
	["바다제비", "Oceanodroma monorhis"],
	["쇠부리슴새", "Puffinus tenuirostris"],
	["슴새", "Calonectris leucomelas"],
	["흰배슴새", "Pterodroma hypoleuca"],
	["신천옹", "Diomedea albatrus (1891년 최후 기록이)"],
	["아비", "Gavia stellata"],
	["쏙독새", "Caprimulgus indicus"],
	["금눈쇠올빼미", "Athene noctua"],
	["긴꼬리올빼미", "Surnia ulula (1967년 최후 기록이)"],
	["긴점박이올빼미", "Strix uralensis"],
	["소쩍새", "Otus scops"],
	["솔부엉이", "Ninox scutulata"],
	["쇠부엉이", "Asio flammeus"],
	["수리부엉이", "Bubo bubo"],
	["올빼미", "Strix aluco"],
	["칡부엉이", "Asio otus"],
	["큰소쩍새", "Otus bakkamoena"],
	["개개비", "Acrocephalus orientalis"],
	["쇠개개비", "Acrocephalus bistrigiceps"],
	["큰부리개개비", "Acrocephalus aedon"],
	["개개비사촌", "Cisticola juncidis"],
	["꼬리치레", "Rhopophilus pekinensis"],
	["개똥지빠귀", "Turdus naumanni eunomus (ssp. in Japan)"],
	["되지빠귀", "Turdus hortulorum"],
	["굴뚝새", "Troglodytes troglodytes"],
	["갈까마귀", "Corvus dauuricus"],
	["까마귀", "Corvus corone"],
	["까치", "Pica pica"],
	["떼까마귀", "Corvus frugilegus"],
	["물까치", "Cyanopica cyana"],
	["어치", "Garrulus glandarius"],
	["잣까마귀", "Nucifraga caryocatactes"],
	["큰부리까마귀", "Corvus macrorhynchos"],
	["북방긴꼬리딱새(별삼광조)", "Terpsiphone paradisi"],
	["긴꼬리딱새(삼광조)", "Terpsiphone atrocaudata"],
	["꾀꼬리", "Oriolus chinensis"],
	["나무발발이", "Certhia familiaris"],
	["동고비", "Sitta europaea"],
	["쇠동고비", "Sitta villosa"],
	["동박새", "Zosterops japonicus"],
	["한국동박새", "Zosterops erythropleurus"],
	["되새", "Fringilla montifringilla"],
	["멋쟁이", "Pyrrhula pyrrhula"],
	["밀화부리", "Eophona migratoria"],
	["방울새", "Carduelis sinica"],
	["솔양진이", "Pinicola enucleator (1959년 최후 기록이)"],
	["솔잣새", "Loxia curvirostra"],
	["쇠홍방울새", "Carduelis hornemanni"],
	["양진이", "Carpodacus roseus"],
	["적원자", "Carpodacus erythrinus"],
	["콩새", "Coccothraustes coccothraustes"],
	["큰부리밀화부리", "Eophona personata"],
	["꼬까직박구리", "Monticola gularis"],
	["딱새", "Phoenicurus auroreus"],
	["바다직박구리", "Monticola solitarius"],
	["솔딱새", "Muscicapa sibirica"],
	["쇠솔딱새", "Muscicapa dauurica"],
	["쇠유리새", "Luscinia cyane"],
	["울새", "Luscinia sibilans"],
	["유리딱새", "Tarsiger cyanurus"],
	["제비딱새", "Muscicapa griseisticta"],
	["큰유리새", "Cyanoptila cyanomelana"],
	["황금새", "Ficedula narcissina"],
	["긴꼬리때까치", "Lanius schach"],
	["때까치", "Lanius bucephalus"],
	["물때까치", "Lanius sphenocercus"],
	["칡때까치", "Lanius tigrinus"],
	["큰재개구마리", "Lanius excubitor"],
	["긴발톱멧새", "Calcarius lapponicus"],
	["꼬까참새", "Emberiza rutila"],
	["멧새", "Emberiza cioides"],
	["무당새", "Emberiza sulphurata"],
	["북방검은머리쑥새", "Emberiza pallasi"],
	["쑥새", "Emberiza rustica"],
	["점박이멧새", "Emberiza jankowskii (1929년 최후 기록이)"],
	["촉새", "Emberiza spodocephala"],
	["물까마귀", "Cinclus pallasii"],
	["바람까마귀", "Dicrurus hottentottus"],
	["멧종다리", "Prunella montanella"],
	["바위종다리", "Prunella collaris"],
	["곤줄박이", "Parus varius"],
	["박새", "Parus major"],
	["북방쇠박새", "Parus montanus"],
	["쇠박새", "Parus palustris"],
	["진박새", "Parus ater"],
	["상모솔새", "Regulus regulus"],
	["북방개개비", "Locustella certhiola"],
	["섬개개비", "Locustella pleskei"],
	["알락꼬리쥐발귀", "Locustella ochotensis"],
	["쥐발귀개개비", "Locustella lanceolata"],
	["큰개개비", "Magalurus pryeri (1962년 최후 기록이)"],
	["긴다리솔새사촌", "Phylloscopus schwarzi"],
	["되솔새", "Phylloscopus tenellipes"],
	["산솔새", "Phylloscopus occipitalis"],
	["솔새사촌", "Phylloscopus fuscatus"],
	["쇠솔새", "Phylloscopus borealis"],
	["홍여새", "Bombycilla japonica"],
	["황여새", "Bombycilla garrulus"],
	["오목눈이", "Aegithalos caudatus"],
	["귀제비", "Hirundo daurica"],
	["제비", "Hirundo rustica"],
	["뿔종다리", "Galerida cristata"],
	["종다리", "Alauda arvensis"],
	["직박구리", "Ixos amaurotis"],
	["북방쇠찌르레기", "Sturnus sturninus"],
	["쇠찌르레기", "Sturnus philippensis"],
	["찌르레기", "Sturnus cineraceus"],
	["참새", "Passer montanus"],
	["섬참새", "Passer rutilans"],
	["팔색조", "Pitta nympha"],
	["할미새사촌", "Pericrocotus divaricatus"],
	["노랑할미새", "Motacilla cinerea"],
	["물레새", "Dendronanthus indicus"],
	["쇠밭종다리", "Anthus godlewskii"],
	["알락할미새", "Motacilla alba"],
	["옅은밭종다리", "Anthus spinoletta"],
	["큰밭종다리", "Anthus richardi"],
	["한국밭종다리", "Anthus roseatus"],
	["흰등밭종다리", "Anthus gustavi"],
	["힝둥새", "Anthus hodgsoni"],
	["섬휘파람새", "Cettia diphone"],
	["숲새", "Urosphena squameiceps"],
	["바늘꼬리칼새", "Hirundapus caudacutus"],
	["칼새", "Apus pacificus"],
	["물총새", "Alcedo atthis"],
	["뿔호반새", "Ceryle lugubris (Megaceryle?) (1949년 최후 기록이)"],
	["청호반새", "Halcyon pileata"],
	["호반새", "Halcyon coromanda"],
	["후투티", "Upupa epops"],
	["대백로", "Egretta alba"],
	["덤불해오라기", "Ixobrychus sinensis"],
	["쇠백로", "Egretta garzetta"],
	["알락해오라기", "Botaurus stellaris"],
	["왜가리", "Ardea cinerea"],
	["중백로", "Egretta intermedia"],
	["큰덤불해오라기", "Ixobrychus eurhythmus"],
	["해오라기", "Nycticorax nycticorax"],
	["따오기", "Nipponia nippon (1979년 최후 기록이)"],
	["저어새", "Platalea minor"],
	["먹황새", "Ciconia nigra"],
	["황새", "Ciconia boyciana"],
	["개구리매", "Circus aeruginosus"],
	["검독수리", "Aquila chrysaetos"],
	["관수리", "Spilornis cheela"],
	["독수리", "Aegypius monachus"],
	["말똥가리", "Buteo buteo"],
	["물수리", "Pandion haliaetus"],
	["뿔매", "Spizaetus nipalensis (1934년 최후 기록이)"],
	["새매", "Accipiter nisus"],
	["솔개", "Milvus lineatus"],
	["수염수리", "Gypaetus barbatus (1918년 최후 기록이)"],
	["알락개구리매", "Circus melanoleucus (melanoleucos?)"],
	["왕새매", "Butastur indicus"],
	["조롱이", "Accipiter gularis"],
	["참매", "Accipiter gentilis"],
	["참수리", "Haliaeetus pelagicus"],
	["큰말똥가리", "Buteo hemilasius"],
	["털발말똥가리", "Buteo lagopus"],
	["항라머리검독수리", "Aquila clanga"],
];
var COLORNAME_LIST=[
["갈색","#964B00"],
["개나리색","#F7E600"],
["검정","#000000"],
["귤색","#F89B00"],
["금색","#FFD700"],
["군청색","#464964"],
["남색","#000080"],
["노랑","#FFD400"],
["녹색","#009900"],
["다홍색","#FF2400"],
["담청색","#3E91B5"],
["데님","#1560BD"],
["등색","#FFB74C"],
["라벤더색","#E6E6FA"],
["라임색","#BFFF00"],
["마리 루즈","#EDACB1"],
["바다색","#0080FF"],
["밝은 보라","#8977AD"],
["밝은 파랑","#4AA8D8"],
["밤색","#800000"],
["베이지색","#F5F5DC"],
["보라","#8B00FF"],
["분홍색","#FF3399"],
["빨강","#FF0000"],
["상아색","#EEE6C4"],
["살구색","#FBCEB1"],
["세루리안 플래시","#0096C6"],
["셀레스테","#b2ffff"],
["시안색","#00FFFF"],
["심홍색","#DC143C"],
["산호색","#F29886"],
["셰필드 스틸","#437299"],
["암청색","#008080"],
["연두색","#81C147"],
["옥색","#0098DA"],
["올리브색","#808000"],
["은색","#C0C0C0"],
["아이보리","#ECE6CC"],
["아쿠아마린","#5E7E9B"],
["에메랄드 그린","#008D62"],
["울트라 마린","#0099A4"],
["자주색","#800080"],
["자홍색","#FF00FF"],
["장미색","#8D192B"],
["주황색","#FF7F00"],
["청록","#005666"],
["청자색","#6937A1"],
["초록색","#008000"],
["카키색","#8F784B"],
["코발트 블루","#00498C"],
["튤립 느와","#392F31"],
["파랑","#0000FF"],
["풀색","#6A8518"],
["프러시안 블루","#003458"],
["하늘색","#50BCDF"],
["하양","#FFFFFF"],
["황토색","#C68A12"],
["회색","#808080"],
]

class DolfinBox {
	constructor( box_hash ) {
		//console.log("box constructor")
		//console.log(box_hash);
		//console.log(Object.keys(box_hash))
		if(Object.keys(box_hash).includes('coords')) {
			//console.log('coords exists');
			this.coords = box_hash['coords'];
			//console.log(this.coords);
		} else {
			//console.log('coords not exists');
		}
		if(Object.keys(box_hash).includes('formidx')) {
			if( editable ) { this.set_form(box_hash['formidx'].parseInt()); }
			this.boxcolor = box_hash['boxcolor'];
			this.boxname = box_hash['boxname'];
		} else {
			this.boxcolor = this.get_random_color();
			this.boxname = this.get_random_name();
		}
		this.visible = true;
		this.selected = false;
	}
	// Getter
	get_coords() {
	  return this.coords;
	}
	set_coords(coords) {
		this.coords = coords;
		this.coord_input.value = String(this.get_coords());
	}

	set_name(name) {
		this.boxname = name;
		if( this.name_input)
			this.name_input.value = this.boxname;
	}
	set_color(color) {
		this.boxcolor = color;
		if( this.color_input)
			this.color_input.value = this.boxcolor;
	}
	get_temp_coords() {
		return this.temp_coords;
	}
	get_random_name() {
        var idx =  Math.floor(Math.random() * BIRDNAME_LIST.length);
        return BIRDNAME_LIST[idx][0];          
    }
    get_random_color() {
        var idx =  Math.floor(Math.random() * COLORNAME_LIST.length);
        return COLORNAME_LIST[idx][0];          
    }
	set_form(a_idx) {
		if( editable ) {
			this.coord_input = document.getElementById("id_finboxes-"+String(a_idx)+"-coords_str");
			if( this.coord_input )
				this.coord_input.value = String(this.get_coords());
			this.name_input = document.getElementById("id_finboxes-"+String(a_idx)+"-boxname");
			if( this.name_input )
				this.name_input.value = this.boxname;
			this.color_input = document.getElementById("id_finboxes-"+String(a_idx)+"-boxcolor");
			if( this.color_input )
				this.color_input.value = this.boxcolor;
			this.delete_input = document.getElementById("id_finboxes-"+String(a_idx)+"-DELETE");
			if( this.delete_input ) {
				this.delete_input.setAttribute("boxindex",a_idx)
				this.delete_input.addEventListener("change", handleCheckboxChange, false);
			}
		}
	}
	show_temp_coords(){
        this.coord_input.value = String(this.get_temp_coords());
		//console.log("coords:",this.get_coords(),"temp_coords:",this.get_temp_coords())
	}
	update_form(){
		//console.log("update form", this.boxname, "coords:",this.coord_input.value, String(this.get_coords()));
        this.coord_input.value = String(this.get_coords());
        this.name_input.value = this.boxname;
		this.color_input.value = this.boxcolor;
	}
	begin_modification() {
		this.temp_coords = [...this.coords];
	}
	end_modification() {
		this.coords = [...this.temp_coords];
	}
	cancel_modification() {
		this.temp_coords = null;
		//this.coords = [...this.original_coords];
	}
	// Method
  }

  function handleCheckboxChange(e){
	//console.log(e);
	idx = this.getAttribute("boxindex");
	//console.log(idx);
	if( this.checked){
		box_list[idx].visible=false;
	} else {
		box_list[idx].visible=true;
	}
	draw();
  }

    var box_list = [];

    function add_form(a_box){
        //e.preventDefault();
        var emptyForm = document.getElementById("empty-form")
        var newForm = emptyForm.cloneNode(true);
        newForm.style.display="block";
        var specimenForm = document.querySelectorAll(".dolfinbox-form");

        var formNum = specimenForm.length-1
        formNum++;

        newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, formNum);
        var container = document.getElementById("dolfinbox-form-container")
        var newRow = container.insertRow();
        newRow.classList.add("text-center");
        newRow.classList.add("dolfinbox-form");
        newRow.innerHTML = newForm.innerHTML;
        var totalForms = document.getElementById("id_finboxes-TOTAL_FORMS")
        totalForms.setAttribute('value', `${formNum+1}`)
		return formNum;
		
    }

    function add_finbox( a_box, a_add_form=false ) {
        [ x1, y1, x2, y2 ] = a_box;
        if(x2 < 0 || x1 > widthImage || x1==x2 || y2 < 0 || y1 > heightImage || y2==y1 ){return;}
        //console.log(a_box);
        //console.log(box_list);
		new_box = new DolfinBox({ coords: a_box });
		box_idx = box_list.length; 
        box_list[box_list.length] = new_box;
		if( a_add_form ) {
			formidx = add_form();
			new_box.set_form(formidx);
		} else {
			new_box.set_form(box_idx);
		}
        //console.log(box_list);
        //fin_list_div = document.getElementById("fin_list");
        //new_fin_div = document.createElement("div");
        //new_fin_div.innerHTML = String(a_box);
        //fin_list_div.appendChild(new_fin_div);
        //add_form(new_box);
		return new_box;
    }


    var LEFT_BUTTON = 0;
    var RIGHT_BUTTON = 2;
    var canvas = document.getElementById("canvas");
    var context = canvas.getContext("2d");

    var widthCanvas, heightCanvas;
	widthCanvas = canvas.width;
	heightCanvas = canvas.height;
	var whratioCanvas = widthCanvas / heightCanvas;

	// mode parameters
	var editable = false;
	var panning = false;
	var drawing_box = false;
	var modifying_box = false;

    var widthImage = 0;
    var heightImage = 0;
    var image_canvas_ratio = 0;
    var downX = 0;
    var downY = 0;
    var box_x1 = -1, box_y1 = -1, box_x2 = -1, box_y2 = -1;
    var mod_x1 = -1, mod_y1 = -1, mod_x2 = -1, mod_y2 = -1;
    var lastupX = 0;
    var lastupY = 0;
    var deltaX = 0;
    var deltaY = 0;
    var scale=1;
	var selected_box = null;

	function draw_rect(a_coords) {
		context.rect( scale_to_canvas(a_coords[0])+lastupX+deltaX, scale_to_canvas(a_coords[1])+lastupY+deltaY, scale_to_canvas(a_coords[2]-a_coords[0]), scale_to_canvas(a_coords[3]-a_coords[1]));
	}
	function draw_line(a_coords, a_line) {
		//console.log("draw line", a_line, a_coords,context.strokeStyle);
		a_coords[0] = scale_to_canvas(a_coords[0])+lastupX+deltaX
		a_coords[1] = scale_to_canvas(a_coords[1])+lastupY+deltaY
		a_coords[2] = scale_to_canvas(a_coords[2])+lastupX+deltaX
		a_coords[3] = scale_to_canvas(a_coords[3])+lastupY+deltaY
		//console.log(a_coords);
		var from_x,from_y,to_x,to_y;
		if(a_line == 'x1'){ from_x=to_x=a_coords[0]; from_y=a_coords[1]; to_y=a_coords[3] }
		if(a_line == 'x2'){ from_x=to_x=a_coords[2]; from_y=a_coords[1]; to_y=a_coords[3] }
		if(a_line == 'y1'){ from_y=to_y=a_coords[1]; from_x=a_coords[0]; to_x=a_coords[2] }
		if(a_line == 'y2'){ from_y=to_y=a_coords[3]; from_x=a_coords[0]; to_x=a_coords[2] }
		context.moveTo( from_x,from_y);
		context.lineTo(to_x,to_y);
	}

    var img = new Image();
    img.src= "{{image.imagefile.url}}";
    img.onload=function(){
        widthImage = img.width;
        heightImage = img.height;
        whratioImage = widthImage / heightImage;
        if( whratioCanvas > whratioImage ) {
            image_canvas_ratio = heightImage / heightCanvas;
        } else {
            image_canvas_ratio = widthImage / widthCanvas;
        }
		if (typeof box_list_data != 'undefined') {
			for( var idx = 0 ; idx < box_list_data.length ; idx++ ) {
				var l_finbox = add_finbox(box_list_data[idx]['coords'],false);
				l_finbox.set_name(box_list_data[idx]['boxname']);
				l_finbox.set_color(box_list_data[idx]['boxcolor']);
				if( box_list_data[idx]['id'] == finid ) {
					selected_box = l_finbox;
				}
				//l_finbox.
			}
		}
		if( selected_box != null )
			focusSelectedBox();

        //console.log("canvas:", widthCanvas, heightCanvas, "image:", widthImage, heightImage);
        //image_canvas_ratio = widthImage/widthCanvas;
        draw();

        //canvas.addEventListener("dblclick", handleDblClick, false);  // dblclick to zoom in at point, shift dblclick to zoom out.
        if( editable == true ) {
            canvas.addEventListener("mousedown", handleMouseDown, false); // click and hold to pan
            canvas.addEventListener("mousemove", handleMouseMove, false);
            canvas.addEventListener("mouseup", handleMouseUp, false);
            canvas.addEventListener("mouseout", handleMouseOut, false);
            canvas.addEventListener("mousewheel", handleMouseWheel, false); // mousewheel duplicates dblclick function
            canvas.addEventListener('contextmenu', (event) => {event.preventDefault();});
            canvas.addEventListener("DOMMouseScroll", handleMouseWheel, false); // for Firefox
			canvas.addEventListener('dblclick', handleDblClick, false );
        }
    }
    function scale_to_canvas( coord ) { return Math.round(( coord / image_canvas_ratio ) * scale); }
    function scale_to_image( coord ) { return Math.round(( coord / scale ) * image_canvas_ratio); }

    function draw() {
        //console.log("draw")

		context.fillStyle='grey';
		context.lineWidth = 2;
        context.fillRect(0,0, widthCanvas,heightCanvas);
        context.drawImage(img,lastupX+deltaX,lastupY+deltaY,(widthImage/image_canvas_ratio)*scale,(heightImage/image_canvas_ratio)*scale);
		//console.log(box_list);
		canvas.style.cursor = 'default';
        for( var i=0;i<box_list.length;i++){
			if(box_list[i].visible) {
				curr_box = box_list[i];
				var _coords = curr_box.get_coords();
				var coords = [..._coords];
				if( curr_box.box_modify ) {
					curr_box.temp_coords = [...coords];
					canvas.style.cursor = curr_box.cursor_style;
					//context.strokeStyle='rgba(255,0,0,0.4)';
					if( curr_box.x1_selected || curr_box.all_selected ) { curr_box.temp_coords[0] += scale_to_image(mod_x2 - mod_x1); }
					if( curr_box.y1_selected || curr_box.all_selected ) { curr_box.temp_coords[1] += scale_to_image(mod_y2 - mod_y1); }
					if( curr_box.x2_selected || curr_box.all_selected ) { curr_box.temp_coords[2] += scale_to_image(mod_x2 - mod_x1); }
					if( curr_box.y2_selected || curr_box.all_selected ) { curr_box.temp_coords[3] += scale_to_image(mod_y2 - mod_y1); }
					coords = [...curr_box.temp_coords]
					curr_box.show_temp_coords();
					//context.strokeStyle='rgba(0,0,0,1)';
				}
				//context.rect( (box[0]/image_canvas_ratio)*scale+lastupX+deltaX, (box[1]/image_canvas_ratio)*scale+lastupY+deltaY, ((box[2]-box[0])/image_canvas_ratio)*scale, ((box[3]-box[1])/image_canvas_ratio)*scale);
				if( curr_box.all_selected ) {
					context.beginPath();
					context.strokeStyle='rgba(255,0,0,1)';
					draw_rect(coords);
					context.stroke();
					context.closePath();
				} else if( !curr_box.box_modify ) {
					context.beginPath();
					context.strokeStyle='rgba(0,0,0,1)';
					draw_rect(coords);
					context.stroke();
					context.closePath();
				} else {
					context.beginPath();
					context.strokeStyle='rgba(0,0,0,1)';
					if( !curr_box.x1_selected ) draw_line([...coords], 'x1');
					if( !curr_box.x2_selected ) draw_line([...coords], 'x2');
					if( !curr_box.y1_selected ) draw_line([...coords], 'y1');
					if( !curr_box.y2_selected ) draw_line([...coords], 'y2');
					context.stroke();
					context.closePath();
					context.beginPath();
					context.strokeStyle='rgba(255,0,0,0.5)';
					if( curr_box.x1_selected ) draw_line([...coords], 'x1');
					if( curr_box.x2_selected ) draw_line([...coords], 'x2');
					if( curr_box.y1_selected ) draw_line([...coords], 'y1');
					if( curr_box.y2_selected ) draw_line([...coords], 'y2');
					context.stroke();
					context.closePath();
				}
			}
        }
        if( drawing_box ) {
            context.beginPath();
            [ draw_x1, draw_y1, draw_x2, draw_y2 ] = [ box_x1, box_y1, box_x2, box_y2 ];
            if( box_x1 > box_x2 ) { [draw_x1, draw_x2] = [box_x2,box_x1];}
            if( box_y1 > box_y2 ) { [draw_y1, draw_y2] = [box_y2,box_y1];}
            context.rect( draw_x1, draw_y1, draw_x2 - draw_x1, draw_y2 - draw_y1 );
            context.stroke();            
        }
    }

    function handleMouseDown(event) {
        //console.log("mouse down");
        if(event.button == RIGHT_BUTTON) {
            panning = true;
            //downX = event.clientX - this.offsetLeft - this.clientLeft + this.scrollLeft;
            //downY = event.clientY - this.offsetTop - this.clientTop + this.scrollTop;
            let box = this.getBoundingClientRect();
            downX = Math.round(event.clientX-box.left);
            downY = Math.round(event.clientY-box.top);
            //console.log("down:",downX,downY);
        } else if( event.button == LEFT_BUTTON ) {
            let box = this.getBoundingClientRect();
			//console.log(selected_box);
			if( selected_box != null ) {
				mod_x1 = Math.round(event.clientX-box.left);
				mod_y1 = Math.round(event.clientY-box.top);
				selected_box.begin_modification();
				modifying_box = true;

			} else {
				box_x1 = Math.round(event.clientX-box.left);
				box_y1 = Math.round(event.clientY-box.top);
				drawing_box = true
			}
        }
    }

    function handleMouseOut(event) {
        //if(event.button == 2) { console.log("right button"); event.preventDefault(); }
        //console.log("mouse out")
        if(panning) {
            lastupX += deltaX;
            lastupY += deltaY;
            deltaX = 0;
            deltaY = 0;
            panning=false;
        } else if( modifying_box ) {
			modifying_box = false;
			[mod_x1,mod_y1,mod_x2,mod_y2]= [0,0,0,0]
			selected_box.cancel_modification();
			selected_box.update_form();
			selected_box = null;
		}
        draw()
    }


    function handleMouseUp(event) {
        //if(event.button == 2) { console.log("right button"); event.preventDefault(); }
        //console.log("mouse up");
		//console.log(selected_box);
        //console.log("mouse up");
        if(event.button == RIGHT_BUTTON) {
            panning = false;
            lastupX += deltaX;
            lastupY += deltaY;
            deltaX = 0;
            deltaY = 0;
        } else if( event.button == LEFT_BUTTON ){
			if( drawing_box ) {
				/* add box */
				drawing_box = false;
				let box = this.getBoundingClientRect();
				box_x2 = Math.round(event.clientX-box.left);
				box_y2 = Math.round(event.clientY-box.top);
				if(box_x1>box_x2){[box_x1,box_x2]=[box_x2,box_x1];}
				if(box_y1>box_y2){[box_y1,box_y2]=[box_y2,box_y1];}
				//console.log( box_x1, box_y1, box_x2, box_y2 );
				real_x1 = Math.max(scale_to_image(box_x1 - lastupX),0);
				real_x2 = Math.min(scale_to_image(box_x2 - lastupX),widthImage);
				real_y1 = Math.max(scale_to_image(box_y1 - lastupY),0);
				real_y2 = Math.min(scale_to_image(box_y2 - lastupY),heightImage);
				//console.log( real_x1, real_y1, real_x2, real_y2 );
				add_finbox([real_x1, real_y1, real_x2, real_y2],true);
				//
				[box_x1,box_y1,box_x2,box_y2] = [-1,-1,-1,-1];
			} else if( modifying_box ) {
				modifying_box = false;
				//console.log(selected_box.get_coords());
				//console.log(selected_box.get_temp_coords());
				if( selected_box.temp_coords[0] > selected_box.temp_coords[2] ) { [ selected_box.temp_coords[0],selected_box.temp_coords[2] ] = [ selected_box.temp_coords[2],selected_box.temp_coords[0] ]; }
				if( selected_box.temp_coords[1] > selected_box.temp_coords[3] ) { [ selected_box.temp_coords[1],selected_box.temp_coords[3] ] = [ selected_box.temp_coords[3],selected_box.temp_coords[1] ]; }

				selected_box.set_coords(selected_box.temp_coords);
				[mod_x1,mod_y1,mod_x2,mod_y2] = [-1,-1,-1,-1];				
				//selected_box = null;
			}
			//console.log("set selected_box null")
        }
		draw();
    }

    
    function handleMouseMove(event) {
        //console.log("mouse move");

        //var X = event.clientX - this.offsetLeft - this.clientLeft + this.scrollLeft;
        //var Y = event.clientY - this.offsetTop - this.clientTop + this.scrollTop;
        let box = this.getBoundingClientRect();
        var X = Math.round(event.clientX-box.left);
        var Y = Math.round(event.clientY-box.top);
		//selected_box = null;

        //console.log(X,event.clientX,box.left,box.top,this.offsetLeft,this.clientLeft,this.scrollLeft,Y,event.clientY,this.offsetTop,this.clientTop,this.scrollTop,lastupX,lastupY);
        //console.log(event.clientX,box.left,event.clientY,box.top,Math.round(event.clientX-box.left),Math.round(event.clientY-box.top));
        if (panning) {
            deltaX = X - downX;
            deltaY = Y - downY;
            //console.log(deltaX,deltaY);
        } else if ( drawing_box ) {
            box_x2 = X;
            box_y2 = Y;
        } else if ( modifying_box ){
            mod_x2 = X;
            mod_y2 = Y;
			//selected_box.show_temp_coords();
			//console.log(selected_box)
        } else {
			//console.log("check nearby box");
			modifying_box_exist = false;
			for( var idx = 0 ; idx < box_list.length ; idx++ ){
				curr_box = box_list[idx]
				coords = curr_box.get_coords()
				x1 = scale_to_canvas(coords[0])+lastupX;
				y1 = scale_to_canvas(coords[1])+lastupY;
				x2 = scale_to_canvas(coords[2])+lastupX;
				y2 = scale_to_canvas(coords[3])+lastupY;
				if(x1>x2){[x1,x2]=[x2,x1];}
				if(y1>y2){[y1,y2]=[y2,y1];}
				//console.log(box_list[idx].get_coords()[0],x1,X)
				NEARBY_THRESHOLD = 10;
				curr_box.box_modify = false;
				curr_box.y_within_box = false;
				curr_box.x_within_box = false;
				curr_box.x1_selected = false;
				curr_box.x2_selected = false;
				curr_box.y1_selected = false;
				curr_box.y2_selected = false;
				curr_box.all_selected = false;
				if( modifying_box_exist ) { curr_box.box_modify = false; continue; }
				if( y1-NEARBY_THRESHOLD < Y && y2+NEARBY_THRESHOLD>Y){
					if( Math.abs(x1 - X)<NEARBY_THRESHOLD ){
						curr_box.cursor_style = 'ew-resize';
						curr_box.x1_selected = true;
						curr_box.box_modify = true;
					} else if ( Math.abs(x2 - X)<NEARBY_THRESHOLD ){
						curr_box.cursor_style = 'ew-resize';
						curr_box.x2_selected = true;
						curr_box.box_modify = true;
					} else if( y1+NEARBY_THRESHOLD < Y && y2-NEARBY_THRESHOLD>Y){
						curr_box.y_within_box = true;
					}
				} 
				if( x1-NEARBY_THRESHOLD < X && x2+NEARBY_THRESHOLD>X){
					if( Math.abs(y1 - Y)<NEARBY_THRESHOLD ){
						curr_box.cursor_style = 'ns-resize';
						curr_box.y1_selected = true;
						curr_box.box_modify = true;
					} else if ( Math.abs(y2 - Y)<NEARBY_THRESHOLD ){
						curr_box.cursor_style = 'ns-resize';
						curr_box.y2_selected = true;
						curr_box.box_modify = true;
					} else if (x1+NEARBY_THRESHOLD < X && x2-NEARBY_THRESHOLD>X){
						curr_box.x_within_box = true;
					}
				}
				if( curr_box.x_within_box && curr_box.y_within_box) { 
					curr_box.all_selected = true;
					curr_box.box_modify = true;
					curr_box.cursor_style = 'move' 
				}
				if( curr_box.x1_selected && curr_box.y1_selected || curr_box.x2_selected && curr_box.y2_selected ) {
					curr_box.cursor_style = 'nwse-resize';
				} else if( curr_box.x1_selected && curr_box.y2_selected || curr_box.x2_selected && curr_box.y1_selected ) {
					curr_box.cursor_style = 'nesw-resize';
				}
				if( curr_box.box_modify ) { 
					//console.log("modifying box", curr_box.boxname );
					modifying_box_exist = true;
					selected_box = curr_box; 
					//console.log("modifying box", curr_box.boxname);
				}				
			}
			if( !modifying_box_exist ) { 
				selected_box = null; 
			} else {
				//console.log("modifying_box_exist:", modifying_box_exist);
				//console.log("selected_box 1:",selected_box.boxname);
			}
		}
        lastX = X;
        lastY = Y;
        draw();
		//console.log("selected_box 2:",selected_box.boxname);

    }

	function focusSelectedBox(){
		if( selected_box != null ){
			var coords = selected_box.get_coords();
			//console.log(coords);
			var center_x = Math.round(( coords[0] + coords[2] ) / 2.0 );
			var center_y = Math.round(( coords[1] + coords[3] ) / 2.0 );
			var rect_halfwidth = coords[2] - coords[0];
			var rect_halfheight = coords[3] - coords[1];
			var rect_whratio = rect_halfwidth / rect_halfheight;

			if( whratioCanvas > rect_whratio ) {
				rect_halfwidth = rect_halfheight * whratioCanvas;
			} else {
				rect_halfheight = rect_halfwidth / whratioCanvas;
			}
			var rect_x1 = center_x - rect_halfwidth;
			var rect_y1 = center_y - rect_halfheight;
			scale = Math.round( ( widthImage / ( rect_halfwidth * 2 ) ) * 10 ) / 10;
			lastupX = -1 * scale_to_canvas(rect_x1);
			lastupY = -1 * scale_to_canvas(rect_y1);
			draw();
		}
	}

	function handleDblClick(event) {
		console.log("double click", selected_box.boxname);
		focusSelectedBox();
	}
		
    function handleMouseWheel(event) {
        //event.stopPropagation();
        //console.log("wheel");

        event.preventDefault();
        var scaleDelta = (event.wheelDelta < 0 || event.detail > 0) ? -0.1 : +0.1;
        if( scale <= 0.8 && scaleDelta < 0 ) {
            //lastupX = 0; lastupY = 0;
            return;
        }
        if( scale > 1 ) scaleDelta *= Math.floor(scale);
        prev_scale = scale;
        scale += scaleDelta;
        scale = Math.round( scale * 10 ) / 10;
        scale_proportion = scale/prev_scale;
        //var X = event.clientX - this.offsetLeft - this.clientLeft + this.scrollLeft;
        //var Y = event.clientY - this.offsetTop - this.clientTop + this.scrollTop;
        let box = this.getBoundingClientRect();

        var X = Math.round(event.clientX-box.left);
        var Y = Math.round(event.clientY-box.top);
        //console.log(X, Y, lastupX, lastupY, scale);
        lastupX = X - ( X - lastupX ) * scale_proportion;
        lastupY = Y - ( Y - lastupY ) * scale_proportion;
        //console.log(X, Y, lastupX, lastupY, scale);
        draw();
    }
