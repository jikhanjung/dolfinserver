<script>
    var box_list = [];
    function add_finbox( a_box ) {
        [ x1, y1, x2, y2 ] = a_box;
        if(x2 < 0 || x1 > widthImage || x1==x2 || y2 < 0 || y1 > heightImage || y2==y1 ){return;}
        console.log(a_box);
        console.log(box_list);
        box_list[box_list.length] = a_box;
        console.log(box_list);
        fin_list_div = document.getElementById("fin_list");
        new_fin_div = document.createElement("div");
        new_fin_div.innerHTML = String(a_box);
        fin_list_div.appendChild(new_fin_div)
    }

    var LEFT_BUTTON = 0;
    var RIGHT_BUTTON = 2;
    var canvas = document.getElementById("canvas");
    var context = canvas.getContext("2d");

    var widthCanvas;
    var heightCanvas;

        // View parameters
    var xleftView = 0;
    var ytopView = 0;
    var widthViewOriginal = 1.0;           //actual width and height of zoomed and panned display
    var heightViewOriginal = 1.0;
    var widthView = widthViewOriginal;           //actual width and height of zoomed and panned display
    var heightView = heightViewOriginal;
    var widthImage = 0;
    var heightImage = 0;
    var image_canvas_ratio = 0;
    var editable = false;
    
    var img = new Image();
    img.src= "{{image.imagefile.url}}";
    img.onload=function(){
        widthCanvas = canvas.width;
        heightCanvas = canvas.height;
        whratioCanvas = widthCanvas / heightCanvas;
        widthImage = img.width;
        heightImage = img.height;
        whratioImage = widthImage / heightImage;
        if( whratioCanvas > whratioImage ) {
            image_canvas_ratio = heightImage / heightCanvas;
        } else {
            image_canvas_ratio = widthImage / widthCanvas;
        }
        //console.log("canvas:", widthCanvas, heightCanvas, "image:", widthImage, heightImage);
        //image_canvas_ratio = widthImage/widthCanvas;
        draw();

        //canvas.addEventListener("dblclick", handleDblClick, false);  // dblclick to zoom in at point, shift dblclick to zoom out.
        if( editable == true ) {

        canvas.addEventListener("mousedown", handleMouseDown, false); // click and hold to pan
        canvas.addEventListener("mousemove", handleMouseMove, false);
        canvas.addEventListener("mouseup", handleMouseUp, false);
        canvas.addEventListener("mousewheel", handleMouseWheel, false); // mousewheel duplicates dblclick function

        canvas.addEventListener('contextmenu', (event) => {event.preventDefault();});
        canvas.addEventListener("DOMMouseScroll", handleMouseWheel, false); // for Firefox
        }
    }
    function scale_to_canvas( coord ) { return Math.round(( coord / image_canvas_ratio ) * scale); }
    function scale_to_image( coord ) { return Math.round(( coord / scale ) * image_canvas_ratio); }
    function draw() {
        context.fillStyle = "grey";
        context.fillRect(0,0, widthCanvas,heightCanvas);
        context.drawImage(img,lastupX+deltaX,lastupY+deltaY,(widthImage/image_canvas_ratio)*scale,(heightImage/image_canvas_ratio)*scale);
        for( var i=0;i<box_list.length;i++){
            box = box_list[i];
            context.beginPath();
            //context.rect( (box[0]/image_canvas_ratio)*scale+lastupX+deltaX, (box[1]/image_canvas_ratio)*scale+lastupY+deltaY, ((box[2]-box[0])/image_canvas_ratio)*scale, ((box[3]-box[1])/image_canvas_ratio)*scale);
            context.rect( scale_to_canvas(box[0])+lastupX+deltaX, scale_to_canvas(box[1])+lastupY+deltaY, scale_to_canvas(box[2]-box[0]), scale_to_canvas(box[3]-box[1]));
            context.stroke();            
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
    
    var panning = false;
    var drawing_box = false;
    var downX = 0;
    var downY = 0;
    var box_x1 = -1, box_y1 = -1, box_x2 = -1, box_y2 = -1;

    function handleMouseDown(event) {
        //console.log("button:", event.button);
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
            box_x1 = Math.round(event.clientX-box.left);
            box_y1 = Math.round(event.clientY-box.top);
            drawing_box = true
        }
    }

    var lastupX = 0;
    var lastupY = 0;
    var deltaX = 0;
    var deltaY = 0;
    var scale=1;
    function handleMouseUp(event) {
        //if(event.button == 2) { console.log("right button"); event.preventDefault(); }
        //console.log("mouse up")
        if(event.button == RIGHT_BUTTON) {
            panning = false;
            lastupX += deltaX;
            lastupY += deltaY;
            deltaX = 0;
            deltaY = 0;
        } else if( event.button == LEFT_BUTTON ){
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
            add_finbox([real_x1, real_y1, real_x2, real_y2]);
            //
            [box_x1,box_y1,box_x2,box_y2] = [-1,-1,-1,-1];
        }
    }

    
    function handleMouseMove(event) {
        //var X = event.clientX - this.offsetLeft - this.clientLeft + this.scrollLeft;
        //var Y = event.clientY - this.offsetTop - this.clientTop + this.scrollTop;
        let box = this.getBoundingClientRect();
        var X = Math.round(event.clientX-box.left);
        var Y = Math.round(event.clientY-box.top);

        //console.log(X,event.clientX,box.left,box.top,this.offsetLeft,this.clientLeft,this.scrollLeft,Y,event.clientY,this.offsetTop,this.clientTop,this.scrollTop,lastupX,lastupY);
        //console.log(event.clientX,box.left,event.clientY,box.top,Math.round(event.clientX-box.left),Math.round(event.clientY-box.top));
        if (panning) {
            deltaX = X - downX;
            deltaY = Y - downY;
            //console.log(deltaX,deltaY);
        } else if ( drawing_box ) {
            box_x2 = X;
            box_y2 = Y;
        }
        lastX = X;
        lastY = Y;
        //console.log(xleftView,ytopView)
        draw();
    }
    function handleMouseWheel(event) {
        //event.stopPropagation();
        //console.log("wheel");
        event.preventDefault();

        var scaleDelta = (event.wheelDelta < 0 || event.detail > 0) ? -0.1 : +0.1;
        if( scale < 0.2 && scaleDelta < 0 ) return;
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
</script>