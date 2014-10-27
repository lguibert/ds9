$(document).ready(function(){
      $('#g102').on("mousemove",function(e){
            tab = getCoordonate(e.pageX, e.pageY, this)
            $('#dataG102 .x').html(tab[0]);
            $('#dataG102 .y').html(tab[1]);
      })
      $('#g141').on("mousemove",function(e){
            tab = getCoordonate(e.pageX, e.pageY, this)
            $('#dataG141 .x').html(tab[0]);
            $('#dataG141 .y').html(tab[1]);
      })
      $('#f110').on("mousemove",function(e){
            tab = getCoordonate(e.pageX, e.pageY, this)
            $('#dataF110 .x').html(tab[0]);
            $('#dataF110 .y').html(tab[1]);
      })
      $('#f160140').on("mousemove",function(e){
            tab = getCoordonate(e.pageX, e.pageY, this)
            $('#dataF160140 .x').html(tab[0]);
            $('#dataF160140 .y').html(tab[1]);
      })
      

      function getCoordonate(x, y, selector){
        dataWidth = $(selector).position().left
        dataHeight = $(selector).position().top
        //paddingLeft = spliter($(selector).css('padding-left'), "px")[0]
        //paddingRight = spliter($(selector).css('padding-right'), "px")[0]
        return [x-dataWidth, y-dataHeight]
      }

      /*function spliter(str, separator){
        return str.split(separator)
      }*/
})