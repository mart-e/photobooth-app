"use strict";(globalThis["webpackChunkqPhotobooth"]=globalThis["webpackChunkqPhotobooth"]||[]).push([[714],{3714:(e,t,l)=>{l.r(t),l.d(t,{default:()=>T});var a=l(9835),i=l(6970);const o={class:"row justify-center q-gutter-sm"},n={class:"absolute-bottom text-subtitle2"};function s(e,t,l,s,r,d){const c=(0,a.up)("q-img"),u=(0,a.up)("q-card"),g=(0,a.up)("q-intersection"),m=(0,a.up)("gallery-image-detail"),p=(0,a.up)("q-dialog"),w=(0,a.up)("q-page");return(0,a.wg)(),(0,a.j4)(w,{padding:""},{default:(0,a.w5)((()=>[(0,a.Uk)((0,i.zw)(d.numberOfImages)+" ",1),(0,a._)("div",o,[((0,a.wg)(!0),(0,a.iD)(a.HY,null,(0,a.Ko)(this.store.gallery.images,((e,t)=>((0,a.wg)(),(0,a.j4)(g,{key:e.id,once:"",class:"preview-item"},{default:(0,a.w5)((()=>[(0,a.Wm)(u,{class:"q-ma-sm",onClick:e=>d.openPic(t)},{default:(0,a.w5)((()=>[(0,a.Wm)(c,{src:d.getImageDetail(t),loading:"lazy","spinner-color":"white",ratio:1},{default:(0,a.w5)((()=>[(0,a._)("div",n,(0,i.zw)(this.store.gallery.images[t].caption),1)])),_:2},1032,["src"])])),_:2},1032,["onClick"])])),_:2},1024)))),128))]),(0,a.Wm)(p,{"transition-show":"jump-up","transition-hide":"jump-down",modelValue:s.showImageDetail,"onUpdate:modelValue":t[0]||(t[0]=e=>s.showImageDetail=e),"full-height":"","full-width":""},{default:(0,a.w5)((()=>[(0,a.Wm)(m,{indexSelected:s.indexSelected},null,8,["indexSelected"])])),_:1},8,["modelValue"])])),_:1})}var r=l(7575),d=l(499);const c={class:"q-pa-none"},u={class:"absolute-bottom-left text-subtitle2"},g={class:"q-gutter-sm"},m=(0,a._)("div",null,"Scan to Download!",-1),p={class:"q-gutter-sm"},w=(0,a._)("div",null,"Start",-1),h={class:"q-gutter-sm"},f=(0,a._)("div",null,"back to gallery",-1);function b(e,t,l,o,n,s){const r=(0,a.up)("swiper-slide"),d=(0,a.up)("swiper"),b=(0,a.up)("q-img"),_=(0,a.up)("q-card-section"),y=(0,a.up)("q-card"),v=(0,a.up)("vue-qrcode"),W=(0,a.up)("q-page-sticky"),k=(0,a.up)("q-icon"),S=(0,a.up)("q-btn"),q=(0,a.up)("q-fab-action"),I=(0,a.up)("q-fab"),x=(0,a.Q2)("close-popup");return(0,a.wg)(),(0,a.iD)("div",c,[(0,a.Wm)(d,{navigation:!0,modules:e.modules,class:"mySwiper"},{default:(0,a.w5)((()=>[(0,a.Wm)(r,null,{default:(0,a.w5)((()=>[(0,a.Uk)("Slide 1")])),_:1}),(0,a.Wm)(r,null,{default:(0,a.w5)((()=>[(0,a.Uk)("Slide 2")])),_:1}),(0,a.Wm)(r,null,{default:(0,a.w5)((()=>[(0,a.Uk)("Slide 3")])),_:1}),(0,a.Wm)(r,null,{default:(0,a.w5)((()=>[(0,a.Uk)("Slide 4")])),_:1}),(0,a.Wm)(r,null,{default:(0,a.w5)((()=>[(0,a.Uk)("Slide 5")])),_:1}),(0,a.Wm)(r,null,{default:(0,a.w5)((()=>[(0,a.Uk)("Slide 6")])),_:1}),(0,a.Wm)(r,null,{default:(0,a.w5)((()=>[(0,a.Uk)("Slide 7")])),_:1}),(0,a.Wm)(r,null,{default:(0,a.w5)((()=>[(0,a.Uk)("Slide 8")])),_:1}),(0,a.Wm)(r,null,{default:(0,a.w5)((()=>[(0,a.Uk)("Slide 9")])),_:1})])),_:1},8,["modules"]),(0,a.Wm)(y,{class:"column bg-image",style:{width:"100%",height:"100%"}},{default:(0,a.w5)((()=>[(0,a.Wm)(_,{class:"col no-padding",align:"center"},{default:(0,a.w5)((()=>[(0,a.Wm)(b,{"spinner-color":"white",loading:"lazy",src:o.store.gallery.images[l.indexSelected]["preview"],style:{"max-width":"100%","max-height":"100%"},fit:"contain"},{default:(0,a.w5)((()=>[(0,a._)("div",u,(0,i.zw)(o.store.gallery.images[l.indexSelected].caption),1)])),_:1},8,["src"])])),_:1})])),_:1}),(0,a.Wm)(W,{position:"top-right",offset:[30,30]},{default:(0,a.w5)((()=>[(0,a._)("div",g,[(0,a.Wm)(v,{type:"image/png",tag:"svg",margin:2,color:{dark:"#111111",light:"#EEEEEE"},options:{width:200,errorCorrectionLevel:"high"},value:s.getImageQrData(l.indexSelected)},null,8,["value"]),m])])),_:1}),(0,a.Wm)(W,{position:"top-left",offset:[20,20]},{default:(0,a.w5)((()=>[(0,a._)("div",p,[(0,a.Wm)(S,{color:"primary","no-caps":"",to:"/"},{default:(0,a.w5)((()=>[(0,a.Wm)(k,{left:"",size:"5em",name:"arrow_back_ios_new"}),w])),_:1})])])),_:1}),(0,a.Wm)(W,{position:"bottom",offset:[0,25]},{default:(0,a.w5)((()=>[(0,a._)("div",h,[(0,a.wy)(((0,a.wg)(),(0,a.j4)(S,{color:"primary","no-caps":""},{default:(0,a.w5)((()=>[(0,a.Wm)(k,{left:"",size:"5em",name:"close"}),f])),_:1})),[[x]]),(0,a.Wm)(S,{label:"next",onOnclick:t[0]||(t[0]=t=>e.currentId="NEXT"),target:"_blank"})])])),_:1}),(0,a.Wm)(W,{position:"bottom-right",offset:[35,35]},{default:(0,a.w5)((()=>[(0,a.Wm)(I,{direction:"up",modelValue:o.fabRight,"onUpdate:modelValue":t[2]||(t[2]=e=>o.fabRight=e),"vertical-actions-align":"right",glossy:"",icon:"keyboard_arrow_up"},{default:(0,a.w5)((()=>[(0,a.wy)((0,a.Wm)(q,{"label-position":"left",icon:"delete",label:"Delete",color:"negative",onClick:t[1]||(t[1]=e=>s.deleteImage(o.store.gallery.images[l.indexSelected]["id"]))},null,512),[[x]]),(0,a.Wm)(S,{"label-position":"left",icon:"download",label:"Download",href:o.store.gallery.images[l.indexSelected]["image"],target:"_blank"},null,8,["href"])])),_:1},8,["modelValue"])])),_:1})])}l(8964);var _=l(528),y=l(6899);new y.Z(".swiper",{direction:"vertical",loop:!0,pagination:{el:".swiper-pagination"},navigation:{nextEl:".swiper-button-next",prevEl:".swiper-button-prev"},scrollbar:{el:".swiper-scrollbar"}});const v={props:{indexSelected:{type:Number,required:!0}},beforeCreate(){console.log(this.indexSelected)},data(){return{}},setup(){const e=(0,r.h)();return{store:e,fabRight:(0,d.iH)(!1)}},components:{VueQrcode:_.ZP},methods:{deleteImage(e){this.$api.get("gallery/delete",{params:{id:e}}).then((e=>{console.log(e),this.store.gallery.images.splice(this.indexSelected,1)})).catch((e=>console.log(e)))},getImageDetail(e,t="thumbnail"){return this.store.gallery.images[e][t]},getImageQrData(e){return String(this.store.serverConfig["EXT_DOWNLOAD_URL"]).replace("{filename}",this.store.gallery.images[e]["filename"])}}};var W=l(1639),k=l(4458),S=l(3190),q=l(335),I=l(627),x=l(8879),D=l(2857),Z=l(9361),Q=l(935),U=l(2146),C=l(9984),E=l.n(C);const j=(0,W.Z)(v,[["render",b]]),P=j;E()(v,"components",{QCard:k.Z,QCardSection:S.Z,QImg:q.Z,QPageSticky:I.Z,QBtn:x.Z,QIcon:D.Z,QFab:Z.Z,QFabAction:Q.Z}),E()(v,"directives",{ClosePopup:U.Z});const z={components:{GalleryImageDetail:P},setup(){const e=(0,r.h)();return{store:e,GalleryImageDetail:P,indexSelected:(0,d.iH)(null),showImageDetail:(0,d.iH)(!1)}},computed:{numberOfImages:{get(){return console.log(Object.keys(this.store.gallery["images"]).length),Object.keys(this.store.gallery["images"]).length}}},mounted(){this.$api.get("gallery/images").then((e=>{console.log(e),this.store.gallery.images=e.data})).catch((e=>console.log(e)))},methods:{getImageDetail(e,t="thumbnail"){return this.store.gallery.images[e][t]},openPic(e){console.log(e),this.indexSelected=e,this.showImageDetail=!0}}};var O=l(9885),V=l(1517),H=l(7743);const R=(0,W.Z)(z,[["render",s],["__scopeId","data-v-57d9794d"]]),T=R;E()(z,"components",{QPage:O.Z,QIntersection:V.Z,QCard:k.Z,QImg:q.Z,QDialog:H.Z})}}]);