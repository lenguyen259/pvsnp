import Mathlib
import PEqualNP.Defs
namespace PEqualNP.Outside.L_gct_196_partial
noncomputable section
namespace Aa
open Finset
abbrev aC:=Fin 4×Fin 7→ℂ
abbrev aH:=Fin 7→ℂ
abbrev row (i:Fin 4):aC→ₗ[ℂ] aH:=LinearMap.funLeft ℂ ℂ fun j=>(i,j)
def aO (M:aC):ℂ:=∑e:Fin 4 ↪ Fin 7,∏r,M (r,e r)
abbrev aHw:=Fin 7×Fin 7×Fin 7×Fin 7
def yH:aHw≃(Fin 4→Fin 7) where
 toFun p:= ![p.1,p.2.1,p.2.2.1,p.2.2.2]
 invFun z:=(z 0,z 1,z 2,z 3)
 left_inv _:=rfl
 right_inv z:=by ext i;fin_cases i<;>rfl
lemma cK (M:aC):
  aO M=∑j,∑l,∑m,∑n,
   if j=l∨j=m∨j=n∨l=m∨l=n∨m=n then 0 else
   M (0,j)*M (1,l)*M (2,m)*M (3,n):=by
 classical
 let u (z:Fin 4→Fin 7):=∏r,M (r,z r)
 have A:aO M=∑z:Fin 4→Fin 7,if Function.Injective z then u z else 0:=by
  let E:=Equiv.subtypeInjectiveEquivEmbedding (Fin 4) (Fin 7)
  change(∑e:Fin 4 ↪ Fin 7,u e)=_;rw[←E.sum_comp (fun e:Fin 4 ↪ Fin 7=>u e),←Finset.sum_filter];exact(Finset.sum_subtype _ (by simp) u).symm
 rw[A,←yH.sum_comp (fun z=>if Function.Injective z then u z else 0)];simp only[Fintype.sum_prod_type];refine sum_congr rfl fun a _=>sum_congr rfl fun b _=>sum_congr rfl fun c _=>sum_congr rfl fun d _=> ?_
 let z:=yH (a,b,c,d)
 have p:z 0=a:=rfl;have q:z 1=b:=rfl;have s:z 2=c:=rfl;have t:z 3=d:=rfl;have f:Function.Injective z↔¬(a=b∨a=c∨a=d∨b=c∨b=d∨c=d):=by
  constructor
  ·intro o;have h (i j:Fin 4) (g:i≠j):z i≠z j:=fun h=>g (o h)
   exact not_or_intro (h 0 1 (by decide)) (not_or_intro (h 0 2 (by decide))
    (not_or_intro (h 0 3 (by decide)) (not_or_intro (h 1 2 (by decide))
      (not_or_intro (h 1 3 (by decide)) (h 2 3 (by decide))))))
  ·intro g i j v;simp only[not_or] at g;fin_cases i<;>fin_cases j<;>first | rfl | grind
 change(if Function.Injective z then u z else 0)=_;by_cases g:a=b∨a=c∨a=d∨b=c∨b=d∨c=d
 ·have k:¬Function.Injective z:=fun h=>f.mp h g
  rw[ite_eq_right k,ite_eq_left g]
 ·rw[ite_eq_left (f.mpr g),ite_eq_right g];change(∏r,M (r,z r))=_;simp[Fin.prod_univ_succ,p,q,s,t,mul_assoc]
lemma lO (L:Submodule ℂ aC) (hL:∀t∈L,aO (1+t)≠0)
  (i:Fin 4):∃f:Module.Dual ℂ aH,f 1=1∧∀t∈L,f (row i t)=0:=by
 classical
 have a:(1:aH)∉L.map (row i):=by rintro⟨t,d,g⟩;apply hL (-t) (L.neg_mem d);apply sum_eq_zero;intro e _;apply Finset.prod_eq_zero (mem_univ i);change(1:ℂ)+ -t (i,e i)=0;have h:t (i,e i)=1:=congrFun g (e i);rw[h];ring
 obtain⟨f,j,b⟩:=Submodule.exists_dual_map_eq_bot_of_notMem a inferInstance;refine⟨(f 1)⁻¹ •f,inv_mul_cancel₀ j,?_⟩;intro t d;have c:f (row i t)∈(L.map (row i)).map f:=⟨_,⟨t,d,rfl⟩,rfl⟩
 rw[b] at c;change f (row i t)=0 at c;change(f 1)⁻¹ *f (row i t)=0;simp[c]
abbrev bK (i:Fin 7):aH:=Pi.single i 1
lemma vG (f:Module.Dual ℂ aH) (b:f 1=1):
  ∃a,f (bK a)≠0:=by
 classical
 by_contra! h;have e:∑a:Fin 7,bK a=(1:aH):=by ext j;simp[bK,Finset.sum_apply,Pi.single_apply]
 rw[←e,map_sum] at b;simp[h] at b
lemma aBr (f g:Module.Dual ℂ aH) (r:f 1=1) (s:g 1=1):
  ∃
   x y:aH,f x=1∧g y=1∧
   ∀c d:Fin 7,c≠d→x c*y d+x d*y c=0:=by
 classical
 by_cases e:∃a,f (bK a)≠0∧g (bK a)≠0
 ·obtain⟨a,k,j⟩:=e;refine⟨(f (bK a))⁻¹ •bK a,(g (bK a))⁻¹ •bK a,
   by simp[k],by simp[j],?_⟩
  intro c d i;by_cases h:a=c
  ·subst c;simp[bK,Ne.symm i]
  ·simp[bK,Pi.single_apply,Ne.symm h]
 ·obtain⟨a,k⟩:=vG f r;obtain⟨b,j⟩:=vG g s;have l:g (bK a)=0:=by by_contra h;exact e ⟨a,k,h⟩
  have n:f (bK b)=0:=by by_contra h;exact e ⟨b,h,j⟩
  have hab:a≠b:=by rintro rfl;exact j l
  refine⟨(f (bK a))⁻¹ •(bK a+bK b),
   (g (bK b))⁻¹ •(bK b-bK a),by simp[k,n],
   by simp[j,l],?_⟩
  intro c d i;by_cases m:c=a
  ·subst c;by_cases q:d=b
   ·subst d;simp[bK,hab,hab.symm]
   ·simp[bK,hab,Ne.symm i,q]
  ·by_cases o:c=b
   ·subst c;by_cases p:d=a
    ·subst d;simp[bK,hab,hab.symm]
    ·simp[bK,m,Ne.symm i,p]
   ·simp[bK,Pi.single_apply,m,o]
lemma cD (M:aC) (i j:Fin 4) (a:i≠j)
  (h:∀c d:Fin 7,c≠d→M (i,c)*M (j,d)+M (i,d)*M (j,c)=0):
  aO M=0:=by
 classical
 let τ:=Equiv.swap i j
 let E:=Equiv.embeddingCongr τ (Equiv.refl (Fin 7))
 let w (e:Fin 4 ↪ Fin 7):=∏r,M (r,e r)
 have f (e:Fin 4 ↪ Fin 7) (r:Fin 4):E e r=e (Equiv.swap i j r):=by change e ((Equiv.swap i j).symm r)=_;rw[Equiv.symm_swap]
 let S:Finset (Fin 4):=(univ.erase i).erase j
 have aAg (e:Fin 4 ↪ Fin 7):
   w e=M (i,e i)*M (j,e j)*∏r∈S,M (r,e r):=by
  change(∏r,M (r,e r))=_;rw[←mul_prod_erase univ (fun r=>M (r,e r)) (mem_univ i),←mul_prod_erase (univ.erase i) (fun r=>M (r,e r)) (mem_erase.mpr ⟨a.symm,mem_univ j⟩)];exact(mul_assoc _ _ _).symm
 have b (e:Fin 4 ↪ Fin 7):w e+w (E e)=0:=by
  have l:(∏r∈S,M (r,E e r))=∏r∈S,M (r,e r):=by
   apply prod_congr rfl;intro r n;obtain⟨k,g,_⟩:=(show r≠j∧r≠i∧r∈univ by simpa[S] using n)
   rw[f,Equiv.swap_apply_of_ne_of_ne g k]
  rw[aAg,aAg,l,f,f];simp only[Equiv.swap_apply_left,Equiv.swap_apply_right];rw[←add_mul,h _ _ (fun m=>a (e.injective m)),zero_mul]
 have zero:(∑e,w e)+(∑e,w e)=0:=by
  calc
   _=(∑e,w e)+(∑e,w (E e)):=by rw[E.sum_comp w]
   _=∑e,(w e+w (E e)):=Finset.sum_add_distrib.symm
   _=0:=sum_eq_zero (fun e _=>b e)
 change(∑e,w e)=0;linear_combination zero/2
lemma lB (L:Submodule ℂ aC) (hL:∀t∈L,aO (1+t)≠0)
  (i j:Fin 4) (w:i≠j):
  Module.finrank ℂ (L.map ((row i).prod (row j)))≤11:=by
 classical
 obtain⟨f,k,s⟩:=lO L hL i;obtain⟨g,l,v⟩:=lO L hL j
 let P:=L.map ((row i).prod (row j))
 let H:=(LinearMap.ker f).prod (LinearMap.ker g)
 have n:P≤H:=by rintro _ ⟨t,b,rfl⟩;exact⟨s t b,v t b⟩
 have a (u:Module.Dual ℂ aH) (C:u 1=1):Module.finrank ℂ (LinearMap.ker u)=6:=by
  have B:u≠0:=by rintro rfl;simp at C
  have h:=Module.Dual.finrank_ker_add_one_of_ne_zero B;have d:Module.finrank ℂ aH=7:=by simp[aH]
  omega
 have dimH:Module.finrank ℂ H=12:=by rw[((LinearMap.ker f).prodEquiv (LinearMap.ker g)).finrank_eq,Module.finrank_prod,a f k,a g l]
 change Module.finrank ℂ P≤11;by_contra! A;have q:P=H:=Submodule.eq_of_le_of_finrank_le n (by omega);obtain⟨x,y,E,F,m⟩:=aBr f g k l;have z:(x-1,y-1)∈P:=by rw[q];exact⟨by simp[LinearMap.mem_ker,E,k],by simp[LinearMap.mem_ker,F,l]⟩
 obtain⟨t,b,r⟩:=z;have o (c):(1+t) (i,c)=x c:=by have e:t (i,c)=x c-1:=congrFun (congrArg Prod.fst r) c;change 1+t (i,c)=x c;rw[e];ring
 have p (c):(1+t) (j,c)=y c:=by have e:t (j,c)=y c-1:=congrFun (congrArg Prod.snd r) c;change 1+t (j,c)=y c;rw[e];ring
 apply hL t b (cD _ i j w ?_);simpa only[o,p] using m
end Aa
namespace Aa
def cW (t:aC):ℂ:=(∑i:Fin 4,∑j,t (i,j))
def pQ (t:aC):ℂ:=(∑j,∑l,if j=l then 0 else ∑a:Fin 4,∑b:Fin 4,if a<b then t (a,j)*t (b,l) else 0)
def pR (t:aC):ℂ:=(∑j,∑l,∑m,if j=l∨j=m∨l=m then 0 else ∑a:Fin 4,∑b:Fin 4,∑c:Fin 4,if a<b∧b<c then t (a,j)*t (b,l)*t (c,m) else 0)
def yW (t:aC):ℂ:=(∑j,∑l,∑m,∑n,if j=l∨j=m∨j=n∨l=m∨l=n∨m=n then 0 else t (0,j)*t (1,l)*t (2,m)*t (3,n))
lemma vH (f:Fin 7→ℂ):
  ∑j,f j=f 0+f 1+f 2+f 3+f 4+f 5+f 6:=by
 simp[Fin.sum_univ_succ];ring
set_option maxRecDepth 262144 in
set_option maxHeartbeats 100000000 in
lemma oD (t:aC):
  aO (1+t)=840+120*cW t+20*pQ t+4*pR t+yW t:=by
 rw[cK];simp(config:={decide:=true}) only[cW,pQ,pR,yW,vH,Fin.sum_univ_four,Pi.add_apply,Pi.one_apply,ite_true,ite_false,add_zero,zero_add];ring
end Aa
end
end PEqualNP.Outside.L_gct_196_partial
