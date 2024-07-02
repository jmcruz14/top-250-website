// import * as d3 from 'd3'
import { sortBy } from 'lodash'
import { isNull, isNumber, chain } from 'lodash'
// import Math from 'Math'

export const useComputeList = () => {

  function calculateAverageRating (data) {
    const listLength = data?.length;
    const nullCount = data?.filter(i => isNull(i?.rating)).length;
    const sum = data?.reduce((a, item) => {
      const rating = item?.rating;
      if (!isNull(rating)) return a + rating;
      return a
    }, 0)
    return (sum / (listLength - nullCount)).toFixed(2)
  }

  /**
   * Computes the average rating of the films in list
   * according to their classic rating. (using histogram)
   * 
   * @param {Object} data 
   * @returns {Number} average_classic_rating
   */
  function calculateAverageClassicRating (data) {
    const listLength = data?.length;  
    const nullCount = data?.filter(i => isNull(i?.classic_rating)).length;
    const sum = data?.reduce((a, item) => {
      const rating = item?.classic_rating;
      if (!isNull(rating)) return a + rating;
      return a
    }, 0)
    return (sum / (listLength - nullCount)).toFixed(2)
  }

  /**
   * 
   * @param {Object} data 
   * @returns {Number}
   */
  function calculateRange (data) {
    const numbersOnly = chain(data)
      .filter(i => i?.rating)
      .map(i => i?.rating)
      .value()
    const max = Math.max(...numbersOnly) // spread array so it checks per number, not the array itself
    const min = Math.min(...numbersOnly)
    const range = max - min

    return range.toFixed(2)
  }

  function calculateMedian (data) {
    const numbersOnly = chain(data)
      .filter(i => i?.rating)
      .map(i => i?.rating)
      .value()
    const length = numbersOnly?.length;

    if (length % 2 !== 0) {
      const midpoint = (length + 1) / 2;
      return numbersOnly[midpoint]
    } else {
      const midpointOne = length / 2;
      const midpointTwo = midpointOne + 1;
      return (midpointOne + midpointTwo) / 2
    }
  }

  /**
   * Get the lowest statistic based on indicated statistic measure.
   * 
   * @param {Object} data     data object
   * @param {String} measure  statistic measure of reference
   */
  function calculateLowestStat (data, measure) {
    try {
      const sortedStat = sortBy(data, o => o[measure])
      return sortedStat[0]
    } catch (e) {
      console.error(`Error catching lowest ${measure}: ${e}`)
      return null
    }
  }

  /**
   * Get the highest statistic based on indicated statistic measure.
   * 
   * @param {Object} data     data object
   * @param {String} measure  statistic measure of reference
   */
  function calculateHighestStat (data, measure) {
    try {
      const sortedStat = sortBy(data, o => o[measure])
      return sortedStat.slice().reverse()[0]
    } catch (e) {
      console.error(`Error catching highest ${measure}: ${e}`)
      return null
    }
  }

  return {
    calculateAverageRating,
    calculateAverageClassicRating,
    calculateRange,
    calculateMedian,
    calculateLowestStat,
    calculateHighestStat
  }
}