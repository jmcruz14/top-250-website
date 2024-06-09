import { format as f, parseISO } from 'date-fns'

// 2020-12-02T13:32:32.647000

/**
 * Converts string to date format
 * 
 * @param {String} date 
 * @param {String} format specified date output according to date-fns docs
 * @returns 
 */
export function getDate (dateString, format) {
  try {
    const date = parseISO(dateString)
    const dateObj = f(date, format)
    return dateObj
  } catch (e) {
    console.warn(`Format specified does not meet date-fns standards: ${e}`)
    return f(dateString, 'yyyy-MM-dd HH:mm:ss.SSS')
  }
}

