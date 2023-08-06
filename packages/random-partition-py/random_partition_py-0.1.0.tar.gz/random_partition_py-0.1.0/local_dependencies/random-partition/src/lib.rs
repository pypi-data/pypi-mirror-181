//! Generate approximately uniformly distributed random integer partitions.
//! So given natural numbers n, k find a sequence of natural (nonzero) p₁, ..., pₖ such
//! that n = ∑ᵢ₌₁ᵏ pᵢ.
use ndarray::{s, Array2, Array3};
use num::integer::div_floor;
use rug::Integer;

pub fn number_of_partitions_into_parts(total: usize, number_of_parts: usize) -> Integer {
    match (number_of_parts, total) {
        (0, 0) => 1.into(),
        (0, _) => 0.into(),
        (_, _) => {
            // Should realistically be able to do this with just two rows - but eh
            // TODO: rewrite this to use only two rows acting as a ring buffer
            let mut counts: Array2<Integer> = Array2::zeros((number_of_parts + 1, total + 1));
            counts[[0, 0]] = 1.into();
            for n in 1..=total {
                counts[[1, n]] = 1.into();
            }
            for k in 2..=number_of_parts {
                counts[[k, k]] = 1.into();
                for n in k + 1..=total {
                    counts[[k, n]] = (&counts[[k, n - k]] + &counts[[k - 1, n - 1]]).into();
                }
            }
            std::mem::take(&mut counts[[number_of_parts, total]])
        }
    }
}

pub fn number_of_partitions_into_parts_with_max(
    total: usize,
    number_of_parts: usize,
    max_part: usize,
) -> Array3<Integer> {
    let mut counts: Array3<Integer> = Array3::zeros((total + 1, number_of_parts + 1, max_part + 1));
    for m in 0..=max_part {
        counts[[0, 0, m]] = 1.into();
        // s
        for k in 1..=number_of_parts {
            for n in k..=std::cmp::min(m * k, total) {
                for i in 0..=div_floor(n, m) {
                    let x = counts[[n - i * m, k - i, m - 1]].clone();
                    counts[[n, k, m]] += x;
                }
            }
        }
    }
    counts
}

fn part_lower_bound(total: usize, number_of_parts: usize) -> usize {
    let m1 = div_floor(total, number_of_parts);
    if total % number_of_parts != 0 {
        m1 + 1
    } else {
        m1
    }
}

fn random_partition_buf_from_table<'a, R: rug::rand::MutRandState>(
    rng: &mut R,
    total: usize,
    number_of_parts: usize,
    buf: &'a mut [usize],
    constrained_part_table: &Array3<Integer>,
) -> &'a mut [usize] {
    let mut remaining_total = total;
    let number_of_possible_partitions = number_of_partitions_into_parts(total, number_of_parts);
    let mut which: Integer = number_of_possible_partitions.random_below(rng) + 1; // rng.gen_range(1.into()..=number_of_possible_partitions); // TODO: random int from 1..=number_of_possible_partitions
    let mut ub = total - number_of_parts + 1;
    let mut lb = part_lower_bound(remaining_total, number_of_parts);
    for (i, remaining_parts) in (1..=number_of_parts).rev().enumerate() {
        let mut count = &constrained_part_table[[remaining_total, remaining_parts, lb]];
        let mut part_size = lb;
        'l: for k in lb..=ub {
            count = &constrained_part_table[[remaining_total, remaining_parts, k]];
            part_size = k;
            if count >= &which {
                count = &constrained_part_table[[remaining_total, remaining_parts, k - 1]];
                break 'l;
            }
        }
        buf[i] = part_size;
        remaining_total -= part_size;
        if remaining_total == 0 {
            break;
        }
        which -= count;
        lb = part_lower_bound(remaining_total, remaining_parts - 1);
        ub = part_size;
    }
    &mut buf[0..number_of_parts]
}

/// Generates a random partition of `total` into `number_of_parts` writing the result into the provided buffer.
///
/// # Returns
/// A slice into the input buffer now containing a random partition with elements ordered in
/// descending order.
///
/// # Arguments
/// * `rng` - the random number generator used
/// * `total` - the number being partitioned
/// * `number_of_parts` - how many pieces the partition should have
/// * `buf` - a buffer with at least enough space for `number_of_parts` integers that the
///     returned values are written into.
pub fn random_partition_buf<'a, R: rug::rand::MutRandState>(
    rng: &mut R,
    total: usize,
    number_of_parts: usize,
    buf: &'a mut [usize],
) -> &'a mut [usize] {
    let ub = total - number_of_parts + 1;
    random_partition_buf_from_table(
        rng,
        total,
        number_of_parts,
        buf,
        &number_of_partitions_into_parts_with_max(total, number_of_parts, ub),
    )
}

/// Generates a random partition of `total` into `number_of_parts`.
///
/// # Returns
/// A vector containing a random partition with elements ordered in descending order.
///
/// # Arguments
/// * `rng` - the random number generator used
/// * `total` - the number being partitioned
/// * `number_of_parts` - how many pieces the partition should have
pub fn random_partition<R: rug::rand::MutRandState>(
    rng: &mut R,
    total: usize,
    number_of_parts: usize,
) -> Vec<usize> {
    let mut partition = vec![0; number_of_parts];
    random_partition_buf(rng, total, number_of_parts, &mut partition);
    partition
}

/// Generates multiple random partitions of `total` into `number_of_parts`.
///
/// # Returns
/// A 2D array where each row represents a partition with elements ordered in descending order.
///
/// # Arguments
/// * `rng` - the random number generator used
/// * `total` - the number being partitioned
/// * `number_of_parts` - how many pieces the partition should have
/// * `number_of_partitions` - the total number of partitions to generate
pub fn random_partitions<R: rug::rand::MutRandState>(
    rng: &mut R,
    total: usize,
    number_of_parts: usize,
    number_of_partitions: usize,
) -> Array2<usize> {
    // This array has to be in row major order - this is the documented standard behaviour of ndarray
    let mut partitions = Array2::zeros((number_of_partitions, number_of_parts));
    let ub = total - number_of_parts + 1;
    let table = number_of_partitions_into_parts_with_max(total, number_of_parts, ub);
    for i in 0..number_of_partitions {
        random_partition_buf_from_table(
            rng,
            total,
            number_of_parts,
            partitions.slice_mut(s![i, ..]).as_slice_mut().unwrap(),
            &table,
        );
    }
    partitions
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn partition_with_max() {
        let sol = number_of_partitions_into_parts_with_max(200, 61, 53);
        assert_eq!(sol[[200, 61, 53]], Integer::from(13253620047_u64));
        assert_eq!(sol[[200, 55, 53]], Integer::from(23898693166_u64));
        assert_eq!(sol[[103, 55, 24]], Integer::from(139935_u64));
        assert_eq!(sol[[103, 5, 24]], Integer::from(119_u64));
    }

    #[test]
    fn random() {
        let mut rng = rug::rand::RandState::new();
        dbg!(random_partition(&mut rng, 500, 23));
        // panic!()
    }

    #[test]
    fn random_parts() {
        let mut rng = rug::rand::RandState::new();
        dbg!(random_partitions(&mut rng, 500, 23, 10));
        // panic!()
    }
}
