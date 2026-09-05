async (page) => {
  const jobs = __JOBS__;
  const results = [];
  for (const job of jobs) {
    const result = await page.evaluate(async (job) => {
      const files = new Array(job.urls.length), errors = [];
      let cursor = 0;
      const worker = async () => {
        while (cursor < job.urls.length) {
          const index = cursor++, item = job.urls[index];
          try {
            const r = await fetch(item.url, {signal:AbortSignal.timeout(20000)});
            if (!r.ok) throw new Error('HTTP ' + r.status);
            if (!(r.headers.get('content-type')||'').startsWith('image/')) throw new Error('Not an image');
            const bytes = new Uint8Array(await r.arrayBuffer());
            if (bytes[0] !== 255 || bytes[1] !== 216) throw new Error('Not a JPEG');
            files[index] = {name:item.name, bytes};
          } catch (e) { errors.push({url:item.url,name:item.name,error:String(e)}); }
        }
      };
      await Promise.all(Array.from({length:8}, worker));
      const enc = new TextEncoder();
      files.push({name:'manifest.json',bytes:enc.encode(JSON.stringify({scene_id:job.id,name:job.name,face_size:job.faceSize,expected:job.urls.length,errors,urls:job.urls},null,2))});
      const table = new Uint32Array(256);
      for (let n=0;n<256;n++){ let c=n; for(let k=0;k<8;k++)c=c&1?0xedb88320^(c>>>1):c>>>1;table[n]=c>>>0; }
      const crc32 = bytes => {let c=0xffffffff;for(const b of bytes)c=table[(c^b)&255]^(c>>>8);return (c^0xffffffff)>>>0;};
      const parts=[], central=[];let offset=0,count=0,centralSize=0,totalBytes=0;
      for(const file of files){
        if(!file)continue;
        const name=enc.encode(file.name), size=file.bytes.length,crc=crc32(file.bytes);
        const h=new Uint8Array(30+name.length),v=new DataView(h.buffer);
        v.setUint32(0,0x04034b50,true);v.setUint16(4,20,true);v.setUint16(6,0x800,true);
        v.setUint32(14,crc,true);v.setUint32(18,size,true);v.setUint32(22,size,true);v.setUint16(26,name.length,true);h.set(name,30);
        parts.push(h,file.bytes);
        const ch=new Uint8Array(46+name.length),cv=new DataView(ch.buffer);
        cv.setUint32(0,0x02014b50,true);cv.setUint16(4,20,true);cv.setUint16(6,20,true);cv.setUint16(8,0x800,true);
        cv.setUint32(16,crc,true);cv.setUint32(20,size,true);cv.setUint32(24,size,true);cv.setUint16(28,name.length,true);cv.setUint32(42,offset,true);ch.set(name,46);
        central.push(ch);centralSize+=ch.length;offset+=h.length+size;count++;totalBytes+=size;
      }
      const end=new Uint8Array(22),ev=new DataView(end.buffer);
      ev.setUint32(0,0x06054b50,true);ev.setUint16(8,count,true);ev.setUint16(10,count,true);ev.setUint32(12,centralSize,true);ev.setUint32(16,offset,true);
      const blob=new Blob([...parts,...central,end],{type:'application/zip'});
      const url=URL.createObjectURL(blob);
      return {url,scene_id:job.id,expected:job.urls.length,downloaded:job.urls.length-errors.length,errors,bytes:totalBytes};
    },job);
    const downloadPromise=page.waitForEvent('download',{timeout:15000});
    await page.evaluate(({url,id})=>{const a=document.createElement('a');a.href=url;a.download=id+'.zip';document.body.append(a);a.click();a.remove();},{url:result.url,id:job.id});
    const download=await downloadPromise;
    await download.saveAs('D:/github项目/blender-mcp-main/wzms/reference/panoramas/tiles/'+job.id+'.zip');
    await page.evaluate(url=>URL.revokeObjectURL(url),result.url);
    const failure=await download.failure();
    delete result.url;
    results.push({...result,save_error:failure});
    if(result.errors.length || failure)break;
  }
  return results;
}
