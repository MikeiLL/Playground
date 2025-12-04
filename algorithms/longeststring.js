/* Return length of longest substr
 - split str into array

*/

function len_longestsubstr(str) {
  let left = 0;
  const seen = {};
  let longest = 0;
  for (let right = 0; right < str.length;right++) {
    console.log({
      "string": str,
      "substring": str.substring(left, right),
      "longest": longest,
      "diff": right - left + 1,
      "left": left,
      "right": right,
      "char": str[right],
      "lastseen": seen[str[right]],
    });
    if (!(str[right] in seen) || seen[str[right]] < left) {
      longest = Math.max(longest, right - left + 1);
    } else {
      left = seen[str[right]] + 1;
    }
    seen[str[right]] = right;
    }
  return longest;
}

console.log(len_longestsubstr("aabcdefghhh"), 8); // bcdefgh
//console.log(len_longestsubstr(""), 0); // 0
//console.log(len_longestsubstr("alphabetical"), 8); // 8
//console.log(len_longestsubstr("alphab"), 5); // lphab
//console.log(len_longestsubstr("aaaaaaaa"), 1); // 1
//console.log(len_longestsubstr("aaababcabcdabcdefagah"), 7); // 6
