



	SOLVER'I CALISTIRMAK ICIN;

1) Kodlar "Spyder 4" adli python derleyicisinde yazilmistir.
Baska bir derleyici kullanilacaksa da Python 2.x surumu icin degil 3.x surumlerini destekleyen versiyonu tercih edilmelidir.
2)logo.ppm,resolver,gui ve naca_profilleri dosyalari ayni dizin altinda bulundurulmalidir.
3)gui dosyasini acip kosturmak yeterlidir. Diger dosylari modul olarak kendisi import edecektir.
4)Arayuz kodlamasinda Python'un kendi kutuphanesi olan "tkinter" kullanildigi icin calistirmak icin ayriyetten bir paket yuklemeye gerek yoktur. 1. maddede belirtildigi gibi Python 3 versiyonun kullanilmasi yeterlidir. (Eger Python 2 kullanilacaksa tkinter yerine Tkinter seklinde revize etmek gerekir)
5)Kanat profilleri icin airfoiltools.com sitesindeki 4 basamakli kanat profilleri kullanilmistir. Yeni naca dosyasi koda eklencegi zaman "naca_profilleri" klasorune SELIG formatinda datalar secilerek gui dosyasindaki "profiller" dosyasina eklenmelidir.
6)Isaretsiz airfoil cizimi ve accuracy secenekleri resolver ve gui dosyalarinda yorum olarak # isareti kisitlanmistir istenirse # isaretleri silinerek aktif hale getirilebilinir.

Iyi calismalar

Umut Atakul

atakulumut@gmail.com


