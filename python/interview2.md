# Python Interview Questions — Part 2: More Problem Solving & Coding Challenges

This is a follow-up to the first guide, focused heavily on algorithmic problem-solving, arrays/strings/trees, and trickier real-world coding questions.

---

## Section 1: Arrays & Lists (Q1–Q15)

**Q1. Find the maximum subarray sum (Kadane's Algorithm).**
```python
def max_subarray(nums):
    max_sum = current_sum = nums[0]
    for n in nums[1:]:
        current_sum = max(n, current_sum + n)
        max_sum = max(max_sum, current_sum)
    return max_sum
```

**Q2. Find all pairs in an array that sum to a target value (not just one pair).**
```python
def all_pairs(nums, target):
    seen = set()
    pairs = set()
    for n in nums:
        complement = target - n
        if complement in seen:
            pairs.add((min(n, complement), max(n, complement)))
        seen.add(n)
    return list(pairs)
```

**Q3. Find the intersection of two arrays.**
```python
def intersection(a, b):
    return list(set(a) & set(b))
```

**Q4. Move all zeros in a list to the end while preserving order of non-zero elements.**
```python
def move_zeros(nums):
    insert_pos = 0
    for n in nums:
        if n != 0:
            nums[insert_pos] = n
            insert_pos += 1
    for i in range(insert_pos, len(nums)):
        nums[i] = 0
    return nums
```

**Q5. Find the equilibrium index of an array (where sum of left elements == sum of right elements).**
```python
def equilibrium_index(nums):
    total = sum(nums)
    left_sum = 0
    for i, n in enumerate(nums):
        total -= n
        if left_sum == total:
            return i
        left_sum += n
    return -1
```

**Q6. Given a list of stock prices, find the maximum profit from a single buy/sell.**
```python
def max_profit(prices):
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit
```

**Q7. Find all triplets in an array that sum to zero (3Sum).**
```python
def three_sum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return result
```

**Q8. Find the k most frequent elements in a list.**
```python
from collections import Counter
def top_k_frequent(nums, k):
    return [item for item, _ in Counter(nums).most_common(k)]
```

**Q9. Rotate a matrix (2D list) 90 degrees clockwise, in place.**
```python
def rotate_matrix(matrix):
    matrix.reverse()
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    return matrix
```

**Q10. Find the longest consecutive sequence in an unsorted array.**
```python
def longest_consecutive(nums):
    num_set = set(nums)
    longest = 0
    for n in num_set:
        if n - 1 not in num_set:   # start of a sequence
            length = 1
            while n + length in num_set:
                length += 1
            longest = max(longest, length)
    return longest
```

**Q11. Given an array, find the product of all elements except self (no division).**
```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    left = 1
    for i in range(n):
        result[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right
        right *= nums[i]
    return result
```

**Q12. Merge overlapping intervals.**
```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```

**Q13. Find the majority element that appears more than n/3 times (if any).**
```python
def majority_n3(nums):
    counts = {}
    for n in nums:
        counts[n] = counts.get(n, 0) + 1
    return [num for num, c in counts.items() if c > len(nums) // 3]
```

**Q14. Implement a function to find the median of two sorted arrays.**
```python
def find_median_sorted_arrays(a, b):
    merged = sorted(a + b)
    n = len(merged)
    mid = n // 2
    if n % 2 == 0:
        return (merged[mid - 1] + merged[mid]) / 2
    return merged[mid]
```
*(Interviewers may ask for an O(log(min(n,m))) binary-search approach for the optimal answer — mention this tradeoff.)*

**Q15. Find the minimum number of swaps to sort an array.**
```python
def min_swaps(arr):
    n = len(arr)
    arr_pos = sorted(range(n), key=lambda i: arr[i])
    visited = [False] * n
    swaps = 0
    for i in range(n):
        if visited[i] or arr_pos[i] == i:
            continue
        cycle_size = 0
        j = i
        while not visited[j]:
            visited[j] = True
            j = arr_pos[j]
            cycle_size += 1
        if cycle_size > 0:
            swaps += cycle_size - 1
    return swaps
```

---

## Section 2: Strings (Q16–Q25)

**Q16. Find the longest substring without repeating characters.**
```python
def longest_unique_substring(s):
    seen = {}
    start = 0
    max_len = 0
    for i, ch in enumerate(s):
        if ch in seen and seen[ch] >= start:
            start = seen[ch] + 1
        seen[ch] = i
        max_len = max(max_len, i - start + 1)
    return max_len
```

**Q17. Check if a string can be rearranged into a palindrome.**
```python
from collections import Counter
def can_form_palindrome(s):
    counts = Counter(s)
    odd_count = sum(1 for c in counts.values() if c % 2 != 0)
    return odd_count <= 1
```

**Q18. Implement basic run-length encoding and decoding.**
```python
def encode(s):
    result = []
    i = 0
    while i < len(s):
        count = 1
        while i + 1 < len(s) and s[i] == s[i + 1]:
            i += 1
            count += 1
        result.append(s[i] + str(count))
        i += 1
    return "".join(result)

def decode(s):
    result = []
    i = 0
    while i < len(s):
        char = s[i]
        j = i + 1
        while j < len(s) and s[j].isdigit():
            j += 1
        result.append(char * int(s[i+1:j]))
        i = j
    return "".join(result)
```

**Q19. Find the minimum window substring containing all characters of another string.**
```python
from collections import Counter
def min_window(s, t):
    if not t or not s:
        return ""
    need = Counter(t)
    missing = len(t)
    left = start = end = 0
    for right, ch in enumerate(s, 1):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:
            while left < right and need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            if end == 0 or right - left < end - start:
                start, end = left, right
            need[s[left]] += 1
            missing += 1
            left += 1
    return s[start:end]
```

**Q20. Group anagrams together from a list of strings.**
```python
from collections import defaultdict
def group_anagrams(words):
    groups = defaultdict(list)
    for word in words:
        key = "".join(sorted(word))
        groups[key].append(word)
    return list(groups.values())
```

**Q21. Implement string compression (e.g., "aabcccccaaa" -> "a2b1c5a3").**
*(Same idea as Q18's `encode`, commonly asked standalone — mention in-place array variants for language-agnostic interviews.)*

**Q22. Check if string `s2` is a rotation of string `s1` in one line.**
```python
def is_rotation(s1, s2):
    return len(s1) == len(s2) and s2 in (s1 + s1)
```

**Q23. Find all substrings of a string that are palindromes.**
```python
def all_palindromic_substrings(s):
    n = len(s)
    result = []
    for i in range(n):
        for j in range(i + 1, n + 1):
            sub = s[i:j]
            if sub == sub[::-1] and len(sub) > 1:
                result.append(sub)
    return result
```

**Q24. Implement basic wildcard pattern matching (`?` and `*`).**
```python
def is_match(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] in (s[i - 1], '?'):
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j - 1] == '*':
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
    return dp[m][n]
```

**Q25. Count the number of vowels and consonants in a string.**
```python
def count_vowels_consonants(s):
    vowels = set("aeiouAEIOU")
    v = sum(1 for ch in s if ch in vowels)
    c = sum(1 for ch in s if ch.isalpha() and ch not in vowels)
    return v, c
```

---

## Section 3: Trees, Graphs & Recursion (Q26–Q35)

**Q26. Implement a binary tree and an in-order traversal.**
```python
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def inorder(root, result=None):
    if result is None:
        result = []
    if root:
        inorder(root.left, result)
        result.append(root.val)
        inorder(root.right, result)
    return result
```

**Q27. Check if a binary tree is a valid Binary Search Tree (BST).**
```python
def is_valid_bst(root, low=float('-inf'), high=float('inf')):
    if not root:
        return True
    if not (low < root.val < high):
        return False
    return (is_valid_bst(root.left, low, root.val) and
            is_valid_bst(root.right, root.val, high))
```

**Q28. Find the maximum depth (height) of a binary tree.**
```python
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

**Q29. Perform a level-order (BFS) traversal of a binary tree.**
```python
from collections import deque
def level_order(root):
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result
```

**Q30. Find the lowest common ancestor (LCA) of two nodes in a BST.**
```python
def lowest_common_ancestor(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
```

**Q31. Implement a graph using an adjacency list and perform DFS.**
```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited
```

**Q32. Implement BFS on a graph to find shortest path (unweighted) between two nodes.**
```python
from collections import deque
def bfs_shortest_path(graph, start, goal):
    queue = deque([[start]])
    visited = {start}
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None
```

**Q33. Detect a cycle in a directed graph.**
```python
def has_cycle(graph):
    visited = set()
    rec_stack = set()

    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(node)
        return False

    return any(dfs(node) for node in graph if node not in visited)
```

**Q34. Solve the classic "number of islands" problem (2D grid, DFS flood fill).**
```python
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    return count
```

**Q35. Implement memoized recursion for climbing stairs (n steps, 1 or 2 at a time).**
```python
from functools import lru_cache
@lru_cache(maxsize=None)
def climb_stairs(n):
    if n <= 2:
        return n
    return climb_stairs(n - 1) + climb_stairs(n - 2)
```

---

## Section 4: Dynamic Programming (Q36–Q42)

**Q36. Solve the classic 0/1 Knapsack problem.**
```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], values[i-1] + dp[i-1][w - weights[i-1]])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][capacity]
```

**Q37. Find the longest common subsequence (LCS) of two strings.**
```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

**Q38. Find the minimum number of coins to make a given amount (Coin Change).**
```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```

**Q39. Find the length of the longest increasing subsequence.**
```python
def longest_increasing_subsequence(nums):
    if not nums:
        return 0
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

**Q40. Solve the "house robber" problem (max sum of non-adjacent elements).**
```python
def rob(nums):
    prev, curr = 0, 0
    for n in nums:
        prev, curr = curr, max(curr, prev + n)
    return curr
```

**Q41. Count the number of unique paths in an m x n grid (only right/down moves).**
```python
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]
```

**Q42. Solve edit distance between two strings (Levenshtein distance).**
```python
def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]
```

---

## Section 5: Real-World / Practical Coding Questions (Q43–Q50)

**Q43. Write a function to validate an email address using regex.**
```python
import re
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None
```

**Q44. Write a decorator that measures a function's execution time.**
```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper
```

**Q45. Write a function to flatten an arbitrarily nested list (any depth).**
```python
def deep_flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(deep_flatten(item))
        else:
            result.append(item)
    return result
```

**Q46. Implement a simple rate limiter (allow N calls per time window).**
```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()

    def allow(self):
        now = time.time()
        while self.calls and self.calls[0] <= now - self.period:
            self.calls.popleft()
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False
```

**Q47. Write a function to chunk a list into batches of size n.**
```python
def chunk_list(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]
```

**Q48. Implement a simple retry decorator with exponential backoff.**
```python
import time
from functools import wraps

def retry(max_attempts=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    time.sleep(base_delay * (2 ** (attempts - 1)))
        return wrapper
    return decorator
```

**Q49. Given a list of `(start, end)` meeting times, determine the minimum number of conference rooms required.**
```python
import heapq
def min_meeting_rooms(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    heap = []  # stores end times
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)
        else:
            heapq.heappush(heap, end)
    return len(heap)
```

**Q50. Write a thread-safe counter class using a lock.**
```python
import threading

class SafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1

    @property
    def value(self):
        with self._lock:
            return self._value
```

---

### Notes for Interview Prep
- For DP problems, always be ready to explain the **recurrence relation** and the **time/space complexity** — interviewers usually ask you to optimize from O(n²) to O(n) space where possible.
- For array/string problems, mention **two-pointer** and **sliding window** patterns explicitly — they show up constantly.
- For graph/tree problems, be comfortable converting between **recursive DFS** and **iterative BFS/stack-based** solutions.
- Always state time and space complexity (Big-O) after solving — interviewers expect this even if not asked directly.
