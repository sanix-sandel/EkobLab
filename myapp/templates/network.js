const input=document.querySelector('input[type="file"]')
input.addEventListener('change', function(e)
{
    const reader=new FileReader()
    reader.onload=function(){
        const lines=reader.result.split('\n').map(function(line){
            return line.split(',')
        })
       
        a="";
        a=lines;
        
        var c=String(lines) 
        n=c.length
        var b=c.slice(1, n-1)
        var d=b.split("],")
        for(var i=0; i<d.length; i++)
        {
          d[i]=d[i].split(",")
        }
    
        alert(d[0][0])
       
       
    }
    reader.readAsText(input.files[0])
}, false)
