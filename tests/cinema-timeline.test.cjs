const {test}=require('node:test');
const assert=require('node:assert/strict');
const {timeline}=require('../scripts/cinema-player.js');
test('timeline handles scene boundaries, scrubbing and the final frame',()=>{
 const reel=timeline([{seconds:8},{seconds:12},{seconds:7}]);
 assert.deepEqual(reel.starts,[0,8,20]);assert.equal(reel.total,27);
 for(const [time,index] of [[0,0],[7.999,0],[8,1],[19.999,1],[20,2],[27,2],[13,1],[2,0]])assert.equal(reel.indexAt(time),index);
});
test('new projects extend the reel without fixed scene indices',()=>{
 const scenes=Array.from({length:100},()=>({seconds:7}));const reel=timeline(scenes);
 assert.equal(reel.total,700);assert.equal(reel.indexAt(699),99);
});
