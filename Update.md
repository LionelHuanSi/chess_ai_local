# Update Plan: Giải thích và hướng nâng cấp Chess AI

## 1. Vì sao con xe đen hay đi qua lại vài ô?

Hiện tượng này thường không phải bug UI, mà là hành vi thường gặp của engine ở mức cơ bản.

### Nguyên nhân chính trong code hiện tại

1. Hàm đánh giá còn quá đơn giản (chỉ đếm vật chất).
- Trong [chess_ai/game/game_logic.py](chess_ai/game/game_logic.py), hàm evaluate gần như chỉ cộng trừ giá trị quân.
- Nếu hai nước đi cho cùng vật chất, engine xem là gần như ngang điểm, nên có thể chọn nước "đi tới đi lui".

2. Độ sâu tìm kiếm còn nông (thường depth=2).
- Engine không nhìn đủ xa để thấy nước lặp là kém kế hoạch.
- Đây là horizon effect: chỉ tối ưu ngắn hạn.

3. Chưa có cơ chế chống lặp vị trí trước khi tới trạng thái hòa chính thức.
- Bạn có xử lý board.is_repetition(3) trong evaluate, nhưng chỉ khi lặp 3 lần mới trả hòa.
- Trước mốc đó, engine vẫn có thể lặp nước vì chưa bị phạt rõ ràng.

4. Alpha-Beta không tự làm engine "thông minh hơn".
- Alpha-Beta chủ yếu giúp cắt nhánh để tính nhanh hơn.
- Chất lượng nước đi vẫn phụ thuộc lớn vào evaluate + độ sâu + move ordering.

## 2. Minimax + Alpha-Beta có điểm yếu không?

Có. Alpha-Beta mạnh về tốc độ tìm kiếm, nhưng vẫn có các hạn chế:

1. Nếu evaluate yếu thì kết quả vẫn yếu.
2. Nếu depth thấp, engine vẫn dễ đi nước "đẹp ngắn hạn".
3. Không có quiescence search thì dễ bị nhiễu tactical (ăn/đổi quân ngay sau đó).
4. Không có transposition table thì lặp lại tính toán cùng vị trí.

Kết luận: Alpha-Beta là nền tảng tốt, nhưng không đủ nếu chưa nâng cấp evaluate và hệ thống search phụ trợ.

## 3. Nên ưu tiên PST + cấu trúc Tốt hay tối ưu hiệu suất nâng cao?

Khuyến nghị: làm cả hai, nhưng theo thứ tự này.

1. Ưu tiên trước: nâng cấp evaluate (PST + cấu trúc Tốt).
- Vì vấn đề bạn gặp (xe đi qua lại) là triệu chứng "thiếu hiểu biết vị trí", không phải thiếu tốc độ thuần.
- PST và pawn structure giúp engine phân biệt rõ hơn giữa các nước có cùng vật chất.

2. Sau đó: tối ưu hiệu suất search.
- Khi evaluate đã tốt hơn, tối ưu hiệu suất giúp đi sâu hơn và phát huy chất lượng evaluate.

## 4. Vai trò từng nâng cấp so với code hiện tại

| Nâng cấp | Vai trò | Khác gì so với hiện tại |
|---|---|---|
| Piece-Square Tables (PST) | Cho điểm theo vị trí quân (trung tâm, phát triển, hậu phương...) | Hiện tại mới đếm vật chất, chưa có điểm vị trí |
| Cấu trúc Tốt | Phạt tốt chồng/cô lập, thưởng tốt thông, chuỗi tốt | Hiện tại chưa có khái niệm cấu trúc tốt |
| Mobility | Thưởng bên có nhiều nước đi hợp lệ, hạn chế bên bị bó | Hiện tại không đo độ cơ động |
| Move Ordering (MVV-LVA, checks first) | Đưa nước "quan trọng" lên trước để cắt tỉa nhiều hơn | Hiện tại duyệt theo thứ tự mặc định |
| Transposition Table | Cache vị trí đã tính để tránh tính lại | Hiện tại mỗi vị trí có thể bị tính nhiều lần |
| Iterative Deepening | Tìm kiếm dần depth 1->2->3..., luôn có best move tạm thời | Hiện tại chạy một depth cố định |
| Quiescence Search | Mở rộng các thế ăn/chiếu ở lá để giảm tactical blunder | Hiện tại dừng cứng ở depth=0 |
| Repetition/Contempt handling | Giảm xu hướng lặp nước hòa khi không cần thiết | Hiện tại chỉ xử lý khi đã lặp 3 lần |

## 5. Roadmap version đề xuất

### Version 1.1 (ổn định hành vi)

1. Thêm tie-break thông minh giữa các nước đồng điểm (ưu tiên phát triển quân, tránh đi ngược lại nước vừa đi nếu không cần).
2. Thêm penalty nhẹ cho lặp vị trí sớm (trước 3-fold draw).
3. Bổ sung logging: số lần lặp vị trí, số lần best move đổi giữa các depth.

Mục tiêu: giảm hiện tượng đi qua đi lại rõ rệt mà không đổi kiến trúc lớn.

### Version 2.0 (nâng chất lượng nước đi)

1. Thêm PST cho Pawn/Knight/Bishop/Rook/Queen/King (midgame trước).
2. Thêm pawn structure score: isolated/doubled/passed pawns.
3. Thêm mobility score cơ bản.

Mục tiêu: engine "biết chơi cờ vị trí" hơn, giảm nước trung tính vô nghĩa.

### Version 3.0 (nâng tốc độ và độ sâu)

1. Move ordering: MVV-LVA cho capture, ưu tiên check, killer/history heuristic.
2. Transposition Table (Zobrist hash).
3. Iterative Deepening + time budget mỗi nước.
4. Quiescence Search cho capture/check sequence.

Mục tiêu: đi sâu hơn nhiều với cùng thời gian, giảm blunder chiến thuật.

## 6. Khuyến nghị thực tế cho bài toán của bạn ngay bây giờ

Nếu chỉ chọn một hướng trước mắt để xử lý hiện tượng xe lặp nước:

1. Làm PST + pawn structure trước.
2. Sau đó thêm move ordering + transposition table.

Lý do:
- Bước 1 giải quyết chất lượng quyết định (đúng bệnh hiện tại).
- Bước 2 tăng độ sâu để quyết định đó ổn định hơn.

## 7. Ghi chú liên quan code hiện tại

- Bạn đã có Alpha-Beta trong [chess_ai/ai/minimax.py](chess_ai/ai/minimax.py).
- Hàm evaluate còn đơn giản trong [chess_ai/game/game_logic.py](chess_ai/game/game_logic.py).
- Vì vậy hiện tượng lặp nước trong nhiều vị trí cân bằng là điều dễ gặp ở phiên bản hiện tại.
