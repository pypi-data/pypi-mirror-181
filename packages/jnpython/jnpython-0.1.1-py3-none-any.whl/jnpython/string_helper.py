
# Manacher's algorithm
def longest_palindrome(s):
    s2 = ''.join(['|']+[c+'|' for c in s])
    palindrome_radii = [0] * (2 * len(s) + 1) # The radius of the longest palindrome centered on each place in S
    center = 0
    radius = 0
    while center < len(s2):
        # Determine the longest palindrome starting at Center-Radius and going to Center+Radius
        while center-(radius+1) >= 0 and center + (radius+1) < len(s2) and s2[center-(radius+1)] == s2[center+(radius+1)]:
            radius += 1
        palindrome_radii[center] = radius

        # increment center, if any precomputed values can be reused, they are
        old_center = center
        old_radius = radius
        center +=1
        radius = 0
        while center <= old_center + old_radius:
            mirrored_center = old_center - (center - old_center)
            max_mirrored_radius = old_center + old_radius - center
            if palindrome_radii[mirrored_center] < max_mirrored_radius:
                palindrome_radii[center] = palindrome_radii[mirrored_center]
                center +=1
            elif palindrome_radii[mirrored_center] > max_mirrored_radius:
                palindrome_radii[center] = max_mirrored_radius
                center +=1
            else: # palindrome_radii[mirrored_center] = max_mirrored_radius
                radius = max_mirrored_radius
                break

    longest_palindrome_in_s = max(palindrome_radii)
    ix = palindrome_radii.index(longest_palindrome_in_s)
    pos = (ix - longest_palindrome_in_s)//2
    palindrome = s[pos:pos+longest_palindrome_in_s]
    return longest_palindrome_in_s, pos, palindrome

def main():
    print(longest_palindrome("kanin"))

if __name__ == "__main__":
    main()