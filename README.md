
# Task hakkında kişisel notlarım ve düşüncelerim:

==NOT: Flutter ve DRF projeleri hakkında açıklamalarım, notlarım  ve istenen kurulum, test vb. direktifler kendi repoları içerisinde olabildiğince profesyonel bir biçimde yazılmıştır. bu dosya daha ziyade projeyi geliştirme sürecimden paylaşmak istediğim noktalara değinecektir. ==

==NOT 2: Bu geri bildirimleri saygı çerçevesinde ve ilgiyle yazmaya özen gösterdim. Lütfen yanlış cümlelerim yada ifadelerim olduysa beni mazur görün. Saygısızlık etmek gibi bir niyetim asla bulunmamakta. Tamamen dürüst ve samimi bir dille kendimi anlatmaya çalıştığımı özellikle belirtmek isterim. Anlayış için teşekkür ediyorum. ^-^==

## 1 - Tech Stack (Kullanılan Teknolojiler)
---
Verilen görevde kullanılması zorunlu kılınan teknolojiler aşina olmayan birinin öğrenip kısa sürede bu denli detaylı ve profesyonel bir sonuç çıkarması için uygun değildi. Neden?

- DRF fazlasıyla soyutlama katmanı, kendine has intrike yapısıyla öğrenme eğrisi oldukça dik olan bir framework. Geleneksel API endpoint geliştirme usulüne kıyasla çok fazla dependency isteyen, Özellikle Django ile fullstack bir app geliştirilmediği senaryoda fazlasıyla karmaşıklık doğuran bir teknoloji. Gerçekten en çok bu soyut yapıyı kavrayıp ezberden kod yazmamış olmak için saatler boyunca çalışma yapmam gerekti. 
- Flutter her ne kadar cross platform bir app UI yazmak için en kestirme yollardan da olsa, aşina olmayan bir kişinin (özellikle web dev geçmişinden geliyorsa) kavramada güçlük çekeceği bir yapıda. Net olmak gerekirse bir dil bile değil, bir Software Development Kit. Yani aslında bir logic ile kurulması için öncelikle ciddi seviyede pratik ve tecrübe gerektiriyor. Ek olarak, geliştirmeye başlamadan önce development env. kurulumu başlı başına dikkat edilmesi gereken ve süreci doğrudan etkileyen bir konu. Özetlemek gerekirse kesinlikle herhangi bir UI lib. yada framework'ü ile kıyaslayacak olursak öğrenme ve introduction seviyesinde hızlı yol katedilecek bir seçenek değil.

Özetle seçilen teknolojileri kullanmayı öğrenmek görevi tamamlamaktan kesinlikle daha zorlayıcıydı. Hatta dürüst olmak gerekirse ve haddimi aşmayacaksam DRF için biraz niş bir tercih bile diyebilirim ^-^ 

## 2 - Görev Kapsamı
---
Özünde görev çok basic bir şekilde API servisi oluşturmamızı ve bununla iletişime geçecek bir UI geliştirmemizi bekliyor. Gayet güzel ve gerçekten de bilgimi sınayacağına inandığım kaliteli bir görev. Ancak, zorunlu koşulan yada tavsiye edilen geliştirme tercihleri daha ziyade bir projede nasıl temiz mimari kurulur ve nasıl profesyonel repo haline getirilir noktasını sınamaya yönlendiriyor.

Zamanımın çok azını projenin mantıksal yönünü düşünmeye ve yazmaya harcarken çoğunu tavsiye edilen test, dokümantasyon paketi vb. şeyleri öğrenmeye çalışırken harcadığımı fark ettim. Üzülerek söylüyorum ki projenin çoğu yerinde ciddi AI yardımı almak zorunda kaldım ve yetiştirebilmek adına pek azını anlayarak yapabildim. Daha basit yapıyla ve daha az dependency ile coding skillerimi gösterebilmeyi dilerdim doğrusu.

## 3 - Projeyi son haline hazırlama süreci
---
Tüm saygımla belirtmek isterim ki proje yönerge dokümanı gayet ciddi bir emek ve planlama sonucu hazırlanmış olduğunu çoğu yönüyle gösteriyor. Ancak new grad. yada junior seviyesinde bir kişinin çoğunun adını dokümanı okurken öğrendiği teknolojilerle gerçekten kendisi yazacaksa bu sürede anlayıp tamamlaması mümkün gelmedi. Çoğu noktada çeşitli LLM lerden yardım aldığımı ve hatta kimi noktalarda yalnızca vibe coding yaptığımı üzülerek itiraf ediyorum. Yine de elimden gelen kadar fazla zamanı ve dikkatimi bu projenin yapımına yoğunlaştırdım.

## 4 - Rastladığım iş duplikasyonları ve mantık hatası içerdiğini (en azından best practise gibi gelmeyen) düşündüğüm noktalar
---
Öncelikle dokümantasyon için kullandığımız OpenAPI ve Swagger + Readme.md içerisinde tekrar tekrar api endpointlerini açıklamak ciddi zaman alan ve bence iş duplikasyonuna sebebiyet veren bir aşama idi.
Bunun üstüne DRF içerisinde hazır bulunan AbstractUser ve bu kadar az field için karmaşık ORM practise leri yapmak biraz emek ve zaman hırsızı idi. Ek olarak zorunlu endpointler içerisinde PATCH (PUT) kullanmaya zorlamak (Benim cehaletim de olabilir ancak neredeyse her senaryoda POST ile yapılmakta) biraz farklıydı. Gerçekten denemek maksadıyla Nodejs ile yazdığımda aynı endpointleri yalnızca GET ve POST requestleri ile yazmam ve bakımlarını yapmam çok daha kısa zamanımı ve satırımı aldı. Ayrıca çok api call anında servis içerisinde sorgu yapmak hız açısından ve anlaşılırlık açısından daha verimsiz geldi (Ekstra sonsuz sayıda anlamlı ve belirgin hedeflere sahip API endpointleri yaratma imkanımız varken).


## Sonuç:
---
Bu noktaya kadar sabırla okuduğunuz için teşekkür ederim. Eğer küstahlık ediyor gibi göründüysem gerçekten böyle bir maksadım olmadığını ve bu geri bildirim + fikirlerimi tamamen ayrılan zaman ve emeğe saygıma karşılık olarak ilgimi belirtmek adına yazdığımı belirtmek isterim.

Üzülerek belirtmeliyim ki görevi beklenen şekilde pürüzsüz ve çalışır halde teslim edemedim. Bunun birincil sebebi bilgi yetersizliği ve buna bağlı olarak süre darlığı idi. Bu projenin tamamını mac (darwin) ortamında geliştirdiğim için özellikle flutter tarafında ciddi bozukluklar deneyimlemeniz olası. bunu mükemmel hale getirmek için zamanım ne yazık ki yeterli olmadı.

Projeyi tamamen AI agentları ile anlama kaygım olmadan hızlıca yazdırmayı gururuma yediremediğim için yer yer saçmalıklar ve eksiklikler göreceksiniz. Şimdiden size sabır diliyorum.

Ayrıca ayırdığı zaman ve ilgi için Mert Bey'e çok teşekkür ediyorum. Süreç boyunca samimi ve destekleyici tavırlarıyla bu deneyimi çok daha değerli hale getirdi.