// int left = 0, right = tLen;  // 能删 0 到全部
// int ans = 0;

// while (left <= right) {
//     int mid = (left + right) / 2;
    
//     if (能匹配(mid)) {  // 删 mid 个后还能得到 p
//         ans = mid;       // 记录一下
//         left = mid + 1;  // 试试能不能删更多
//     } else {
//         right = mid - 1; // 删太多了，少删点
//     }
// }
//通用模板左闭右闭