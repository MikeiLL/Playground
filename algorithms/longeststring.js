/* Return length of longest substr
 - split str into array
 - seen dictionary
 - start
 - cur
 1. cur and start at 0
 2. while cur < arr.length
  add cur to seen with value of position
*/
function len_longestsubstr(str) {
  if (str.length === 0) return "";
  let start = 0;
  let cur = 0;
  const arr = str.split("");
  let longest = [];
  let seen = {};
  while (cur < arr.length) {
    curVal = arr[cur];
    if (curVal in seen) {
      console.log("seen ", curVal);
      start++;
    } else {
      console.log("not seen ", curVal);
    }
    seen[curVal] = cur;
    cur++;
    if (longest.length < (cur+1 - start)) {
      //console.log("reset longest", longest, start, cur);
      longest = arr.slice(start, cur);
      console.log("new longest", longest, start, cur);
      /*
      alphab
       |  |
      */
    } else longest.push(curVal);
    /* console.log({
      "string": str,
      "longest": longest.join(""),
      "longest len": longest.length,
      "cur - start": cur - start,
      "LETTER": curVal, "start": start, "cur": cur, "seen": seen
    }); */
  }
  return longest.join('');
}

// console.log(len_longestsubstr("aabcdefghhh")); // bcdefgh
// console.log(len_longestsubstr("")); // 0
//console.log(len_longestsubstr("alphabetical")); // 8
console.log(len_longestsubstr("alphab")); // lphab
// console.log(len_longestsubstr("aaaaaaaa")); // 1
// console.log(len_longestsubstr("aaababcabcdabcdefagah")); // 6

// start arr[start] == a
// cur arr[1] == a
// "alphabetical"
//   |  |
